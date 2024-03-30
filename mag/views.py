from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import logout as auth_logout  # Renommer la fonction de déconnexion


# Création des différentes vues

class indexView(View):
    def get(self, request, *args, **kwargs):
        latest_post = Post.objects.order_by('-pub_date')[:5]
        latest_news = News.objects.order_by('-pub_date')[:3]
        popular_news = News.objects.order_by('-likes')[:5]
        popular_posts = Post.objects.order_by('-likes')[:4]
        featured_posts = Post.objects.filter(featured=True).order_by('-pub_date')[:3]

        context = {
            'latest_post': latest_post,
            'latest_news': latest_news,
            'popular_news': popular_news,
            'popular_posts': popular_posts,
            'featured_posts': featured_posts,
        }
        return render(request, 'mag/post_template.html', context)

#         Finally, you can display the most liked posts in your index.html template using the following code:

# html
# Copy code
# {% for post in most_liked_posts %}
#     <!-- Display the post here -->
# {% endfor %}

class SignupView(generic.View):
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
            return render(self.request, 'signup.html',
                          {'user_creation_form': userForm, 'utilisateurform': utilisateur_form})

class Signinview(generic.View):
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

@login_required()
def signoutview(request):
    logout(request)
    return redirect('mag:signin')

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

@login_required
def category_post(request, name):
    category = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(Category=Category)
    context = {
        'Category': Category,
        'posts': posts,
    }
    return render(request, 'mag/category_post.html', context)

@login_required
def logout(request):
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL )

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
@login_required
def post_detail(request, pk):
    # Récupérer le post actuel
    post = get_object_or_404(Post, pk=pk)

    # Récupérer les articles ayant la même catégorie que le post actuel
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)
    # Récupérer les commentaires associés à ce post
    comments = Comment.objects.filter(post=post)


    # Passer les données à votre template
    return render(request, 'mag/post_detail.html', {'post': post, 'related_posts': related_posts, 'comments': comments})

@login_required
def news_detail(request, pk):
    post = get_object_or_404(News, pk=pk)
    related_news = News.objects.filter(category=post.category).exclude(pk=post.pk)
    comments = Comment.objects.filter(post=post)

    return render(request, 'mag/news_details.html', {'post': post, 'related_posts': related_news, 'comments': comments})

def terms_of_use(request):
        return render(request, 'mag/terms_of_use.html',)

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