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
from django.views.generic import FormView
from .forms import *

# Importations Django Models
from .models import *

# Importations Django Views
from django.views import generic, View

# Importations supplémentaires de Django
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy


class indexView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        # categoriesNews = CategoryNews.objects.all()
        latest_post = Post.objects.order_by('-pub_date')[:5]
        latest_news = News.objects.order_by('-pub_date')[:3]
        popular_news = News.objects.order_by('-likes')[:5]
        popular_posts = Post.objects.order_by('-likes')[:4]
        featured_posts = Post.objects.filter(featured=True).order_by('-pub_date')[:3]

        context = {
            'categories' : categories,
            #'categoriesNews' : categoriesNews,
            'latest_post': latest_post,
            'latest_news': latest_news,
            'popular_news': popular_news,
            'popular_posts': popular_posts,
            'featured_posts': featured_posts,
        }
        return render(request, 'mag/post_template.html', context)
        
# class SignupView(generic.View):
    def get(self, *args, **kwargs):
        context = {
            'user_creation_form': CreateUserForm(),
            'utilisateurform': UtilisateurForm()
        }
        return render(self.request, 'mag/signup.html', context)

    def post(self, *args, **kwargs):
        userForm = CreateUserForm(data=self.request.POST)
        utilisateur_form = UtilisateurForm(data=self.request.POST)

        if userForm.is_valid() and utilisateur_form.is_valid():
            user = userForm.save(commit=False)
            # on vérifie si l'email existe déjà
            verifEmail = User.objects.filter(email=user.email)
            if verifEmail.count():
                messages.error(self.request,
                               'Cette adresse Email existe déjà. Connectez-vous avec cette adresse ou créez-en une autre')
                return render(self.request, 'signup.html',
                              {'user_creation_form': userForm, 'utilisateurform': utilisateur_form})
            else:
                user.username = user.email
                name = user.first_name
                user.first_name = name.split(' ')[0]
                user.last_name = name.split(' ')[-1]
                user.save()

                utilisateur = utilisateur_form.save(commit=False)
                utilisateur.user = user
                utilisateur.save()

                messages.success(self.request, 'Votre Compte a bien été crée. Connectez-vous et parcourez nos différents articles')

                return redirect('mag:signin')
        else:
            messages.error(self.request, 'Un problème est survenue. Réessayez')
            return render(self.request, 'signup.html', {'user_creation_form': userForm, 'utilisateurform': utilisateur_form})

# class Signinview(generic.View):
    def get(self, *args, **kwargs):
        return render(self.request, 'mag/login.html')

    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            if user.is_active:
                login(self.request, user)
                return redirect('mag:index')
            else:
                messages.error(self.request, 'Votre compte a été désactivé')
                return redirect('mag:signin')
        else:
            messages.error(self.request, "S'il vous plait utilisez un mot de passe ou une adresse email correcte")
            return redirect('mag:signin')

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
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Un problème est survenu lors de la création de votre compte. Veuillez réessayer.')
            return super().form_invalid(form)


class SigninView(FormView):
    template_name = 'mag/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('mag:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Vous êtes maintenant connecté.')
        print("Redirection vers :", self.get_success_url())
        return HttpResponseRedirect('mag:index')
    def form_invalid(self, form):
        messages.error(self.request, "Veuillez vérifier vos informations de connexion.")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("Vous êtes déjà authentifié. Redirection...")
            return HttpResponseRedirect('mag:index')
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
def profile(request):
    utilisateur_form = UtilisateurForm(instance=request.user.utilisateur)
    password_form = PasswordChangeForm()

    if request.method == 'POST':
        utilisateur_form = UtilisateurForm(request.POST, instance=request.user.utilisateur)
        password_form = PasswordChangeForm(request.POST)

        if utilisateur_form.is_valid():
            utilisateur_form.save()

        if password_form.is_valid():
            password = password_form.cleaned_data['password']
            confirm_password = password_form.cleaned_data['confirm_password']
            if password == confirm_password:
                user = request.user
                user.set_password(password)
                user.save()
                return redirect('profile')

    return render(request, 'profile.html', {'utilisateur_form': utilisateur_form, 'password_form': password_form})

def about_us(request):
    return render(request, 'mag/about_us.html')

def index_partenaire(request):
    return render(request, 'mag/index_partenaire.html')

def contact_Us(request):
    return render(request, 'mag/contact_us.html')
 
def FAQ(request):
    return render(request, 'mag/faq.html')

def post_detail_template(request):
    return render(request, 'mag/post_detail_template.html')

def index_partenaire(request):
    return render(request, 'mag/indexpartenaire.html')

def post_detail_template2(request):
    return render(request, 'mag/post_detail_template2.html')

@login_required
def category_post(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    posts = Post.objects.filter(Category=category)
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'mag/category_post.html', context)

class CategoryPostListView(ListView):
    model = Post
    template_name = 'category_post.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Post.objects.filter(Category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        context['category'] = category
        return context

@login_required
def category_news(request, name):
    category_current_one = get_object_or_404(Category, name=name)
    news = News.objects.filter(Category=Category)
    context = {
        'Category': Category,
        'news': news,
    }
    return render(request, 'mag/category_news.html', context)
#je dois finir avec la fonction related_posts dans post_detail et dans news_detail

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Créez une instance de commentaire mais ne l'enregistrez pas encore dans la base de données
            new_comment = form.save(commit=False)
            new_comment.post = post  # Associez le commentaire à l'article actuel
            new_comment.save()  # Enregistrez le commentaire dans la base de données
            return redirect('post_detail', pk=pk)  # Redirigez vers la même page après avoir ajouté le commentaire
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})


# @login_required
# def news_detail(request, pk):
#     post = get_object_or_404(News, pk=pk)
#     related_news = News.objects.filter(category=post.category).exclude(pk=post.pk)
#     comments = Comment.objects.filter(post=post)

#     return render(request, 'mag/news_details.html', {'post': post, 'related_posts': related_news, 'comments': comments})

def terms_of_use(request):
    return render(request, 'mag/terms_of_use.html',)

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    related_news = News.objects.filter(category=news.category).exclude(pk=news.pk)
    comments = Comment.objects.filter(news=news).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.news = news
            new_comment.save()
            return redirect('mag/news_details.html', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'mag/news_details.html', {'news': news, 'related_news': related_news, 'comments': comments, 'form': form})


@login_required
def search_feature(request):
    queryset = Post.objects.all()
    query = ''
    if request.method == 'POST':
        query = request.POST['search_query']
        queryset = queryset.filter(title__contains=query)
    return render(request, 'mag/search_posts.html', {'query': query, 'posts': queryset})

# def search_feature(request):
#     # Check if the request is a post request.
#     if request.method == 'POST':
#         # Retrieve the search query entered by the user
#         search_query = request.POST['search_query']
#         # Filter your model by the search query
#         posts = Post.objects.filter(title__contains=search_query)
#         return render(request, 'mag/search_posts.html', {'query':search_query, 'posts':posts})
#     else:
#         return render(request, 'mag/search_posts.html',{})
    
# @login_required
# def search(request): 
#     queryset = Post.objects.all()
#     query = request.GET.get('q')
#     if query:
#         queryset = queryset.filter(
#             Q(title__icontains=query)  | 
#             Q(title__icontains)
#         )