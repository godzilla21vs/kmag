# Importation des fonctions Django raccourcies
from django.contrib.auth import logout as auth_logout
from django.views.generic.edit import FormView
from django.views.generic import FormView, ListView
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

# Regrouper les importations par catégorie
# Importations Django
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Importations Django auth
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Importations Django Forms
from django.views.generic import TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView
from .forms import *

# Importations Django Models
from .models import *

# Importations Django Views
from django.views import generic, View

# Importations supplémentaires de Django
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
# Importations pour Json
from django.http import JsonResponse

class indexView(View):
    def get(self, request, *args, **kwargs):
        author_kimi_team = Author.objects.filter(name='kimi team').first()
        categories = Category.objects.values_list('name', flat=True)
        partners = Author.objects.exclude(name="kimi team").values_list('name', flat=True)
        latest_post = Post.objects.filter(Author=author_kimi_team).order_by('-pub_date')[:5]
        latest_news = News.objects.filter(Author=author_kimi_team).order_by('-pub_date')[:3]
        popular_news = News.objects.filter(Author=author_kimi_team).order_by('-likes')[:5]
        popular_posts = Post.objects.filter(Author=author_kimi_team).order_by('-likes')[:4]
        featured_posts = Post.objects.filter(featured=True, Author=author_kimi_team).order_by('-pub_date')[:4]

        context = {
            'partners' : partners,
            'categories' : categories,
            #'categoriesNews' : categoriesNews,
            'latest_post': latest_post,
            'latest_news': latest_news,
            'popular_news': popular_news,
            'popular_posts': popular_posts,
            'featured_posts': featured_posts,
        }
        return render(request, 'mag/index.html', context)


class SignupView(FormView):
    template_name = 'mag/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('mag:signin')

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.first_name = user.first_name.split(' ')[0]
        user.last_name = user.first_name.split(' ')[-1]
        user.save()
        utilisateur_form = UtilisateurForm(data=self.request.POST)
        if utilisateur_form.is_valid():
            utilisateur = utilisateur_form.save(commit=False)
            utilisateur.user = user
            utilisateur.save()
            messages.success(self.request, 'Votre compte a bien été créé. Connectez-vous et parcourez nos différents articles')
            return redirect(reverse_lazy('mag:signin'))
        else:
            messages.error(self.request, 'Un problème est survenu lors de la création de votre compte. Veuillez réessayer.')
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['utilisateur_form'] = UtilisateurForm()  # Ajoutez cette ligne pour passer le formulaire d'utilisateur à votre template
        return context

def indexpartner(request, author_name):
        author = Author.objects.get(name=author_name)
        latest_post = Post.objects.filter(Author=author).order_by('-pub_date')[:5]
        latest_news = News.objects.filter(Author=author).order_by('-pub_date')[:3]
        popular_news = News.objects.filter(Author=author).order_by('-likes')[:5]
        popular_posts = Post.objects.filter(Author=author).order_by('-likes')[:4]
        featured_posts = Post.objects.filter(featured=True, Author=author).order_by('-pub_date')[:4]

        # Récupérer les images associées aux derniers posts
        for post in latest_post:
            post.main_image = post.mainimage.image if post.mainimage else None
            thumbnails = Thumbnail.objects.filter(post=post)
            post.thumbnails = thumbnails

        # Récupérer les images associées aux dernières news
        for news in latest_news:
            news.main_image = news.mainimagenews.image if news.mainimagenews else None
            thumbnails = ThumbnailNews.objects.filter(News=news)
            news.thumbnails = thumbnails
        
        for post in popular_posts:
            post.main_image = post.mainimage.image if post.mainimage else None
            thumbnails = Thumbnail.objects.filter(post=post)
            post.thumbnails = thumbnails

        for news in popular_news:
            news.main_image = news.mainimagenews.image if news.mainimagenews else None
            thumbnails = ThumbnailNews.objects.filter(News=news)
            news.thumbnails = thumbnails

        for post in featured_posts:
            post.main_image = post.mainimage.image if post.mainimage else None
            thumbnails = Thumbnail.objects.filter(post=post)
            post.thumbnails = thumbnails

        context = {
            'latest_post': latest_post,
            'latest_news': latest_news,
            'popular_news': popular_news,
            'popular_posts': popular_posts,
            'featured_posts': featured_posts,
        }
        return render(request, 'mag/indexpartner.html', context)

class SigninView(FormView):
    template_name = 'mag/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('mag:index')  # Use reverse_lazy to get the URL

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Vous êtes maintenant connecté.')
        return super().form_valid(form)  # Return the super method

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez vérifier vos informations de connexion.")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('mag:index'))  # Redirect using reverse_lazy
        return super().get(request, *args, **kwargs)

@login_required
def signoutview(request):
    """
    Déconnecte l'utilisateur et le redirige vers la page de connexion.
    """
    auth_logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('mag:signin')

@login_required
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'mag/profile.html'
    utilisateur_form_class = UtilisateurForm
    password_form_class = PasswordChangeForm
    success_url = reverse_lazy('mag:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['utilisateur_form'] = self.utilisateur_form_class(instance=self.request.user.utilisateur)
        context['password_form'] = self.password_form_class()
        return context

    def post(self, request, *args, **kwargs):
        utilisateur_form = self.utilisateur_form_class(request.POST, instance=request.user.utilisateur)
        password_form = self.password_form_class(request.POST)

        if utilisateur_form.is_valid():
            utilisateur_form.save()

        if password_form.is_valid():
            password = password_form.cleaned_data['password']
            confirm_password = password_form.cleaned_data['confirm_password']
            if password == confirm_password:
                user = request.user
                user.set_password(password)
                user.save()
                return redirect(self.success_url)

        return self.render_to_response(self.get_context_data())    
    

def about_us(request):
    return render(request, 'mag/about_us.html')

def index_partenaire(request, author_name):
    author = Author.objects.get(name=author_name)
    # Récupérer tous les posts de cet auteur
    posts = Post.objects.filter(Author=author)
    # Récupérer toutes les news de cet auteur
    news = News.objects.filter(Author=author)
    # Passez les publications à votre template
    context = {
        'author_name': author_name,
        'posts': posts,
        'news': news,
    }
    return render(request, 'mag/index_partenaire.html')

def contact_Us(request):
    return render(request, 'mag/contact_us.html')
 
def FAQ(request):
    return render(request, 'mag/faq.html')

def post_detail_template(request):
    return render(request, 'mag/post_detail_template.html')

def posts_and_news_by_author(request, author_name):
    author = Author.objects.get(name=author_name)
    posts = Post.objects.filter(Author=author)
    news = News.objects.filter(Author=author)
    categories = Category.objects.all()
    context = {
        'author_name': author_name,
        'posts': posts,
        'news': news,
        'categories': categories
    }
    return render(request, '.html', context)

@login_required
def category(request, category_name):
    category = get_object_or_404(Category, name=category_name)

    # Récupérer tous les posts et news de cette catégorie
    posts = Post.objects.filter(Category=category)
    news = News.objects.filter(Category=category)

    # Passer les posts et les news à votre template
    context = {
        'category_name': category_name,
        'posts': posts,
        'news': news,
    }
    return render(request, 'mag/category.html', context)
#je dois finir avec la fonction related_posts dans post_detail et dans news_detail def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(Category=post.Category).exclude(pk=post.pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    num_comments = post.comments.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post  # Fixed: Changed 'new_comment.news' to 'new_comment.post'
            new_comment.save()
            return redirect('mag:post_detail', pk=pk)
    else:
        form = CommentForm()

@login_required
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    related_posts = Post.objects.filter(Category=post.Category).exclude(pk=pk)[:3]  # Assuming you want related posts from the same category
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    num_comments = comments.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('mag:post_detail', pk=pk)
    else:
        form = CommentForm()

    # Handling Post Views
    if not PostSeen.objects.filter(utilisateur_id=request.user.id, post=post).exists():  # Fixed: Changed 'utilisateur' to 'utilisateur_id'
        PostSeen.objects.create(utilisateur_id=request.user.id, post=post)  # Fixed: Changed 'utilisateur' to 'utilisateur_id'
        post.numberView += 1
        post.save()

    # Handling Likes

    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'num_comments': num_comments,
        'form': form
    }
    return render(request, 'mag/post_details.html', context)

@ login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        return JsonResponse({'result': result, })

def terms_of_use(request):
    return render(request, 'mag/terms_of_use.html',)

@login_required
def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    related_news = News.objects.filter(Category=news.Category).exclude(pk=news.pk)
    comments = CommentNews.objects.filter(news=news).order_by('-created_at')
    num_comments = news.commentsNews.count()

    if request.method == 'POST':
        form = CommentNewsForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.news = news
            new_comment.save()
            return redirect('mag/news_details.html', pk=pk)
    else:
        form = CommentNewsForm()
        
    # Gérer les vues
    if not newsSeen.objects.filter(utilisateur=request.user, news=news).exists():
        newsSeen.objects.create(utilisateur=request.user, news=news)
        news.numberView += 1
        news.save()

    # Gérer les likes

    context = {
        'news': news,
        'related_news': related_news,
        'comments': comments,
        'num_comments': num_comments,
        # 'is_liked': is_liked,
        'form': form
    }

    return render(request, 'mag/news_details.html', context)


@login_required
def search_feature(request):
    queryset = Post.objects.all()
    query = ''
    if request.method == 'POST':
        query = request.POST['search_query']
        queryset = queryset.filter(title__contains=query)
    return render(request, 'mag/search_results.html', {'query': query, 'posts': queryset})

