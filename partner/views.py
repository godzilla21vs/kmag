from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.views.generic import FormView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import *
from ..models import *

def index(request):
    return render(request, 'partner/index.html', {'year': 2024})

class SigninView(FormView):
    template_name = 'partner/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('partner:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Vous êtes maintenant connecté.')
        print("Redirection vers :", self.get_success_url())
        return HttpResponseRedirect(reverse_lazy('partner:index'))
    
    def form_invalid(self, form):
        messages.error(self.request, "Veuillez vérifier vos informations de connexion.")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("Vous êtes déjà authentifié. Redirection...")
            return HttpResponseRedirect(reverse_lazy('partner:index'))
        return super().get(request, *args, **kwargs)

@login_required
def signoutview(request):
    """
    Déconnecte l'utilisateur et le redirige vers la page de connexion.
    """
    auth_logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('partner:signin')

def contact_Us(request):
    return render(request, 'partner/contact_us.html')
class PostListView(ListView):
    model = Post
    template_name = 'partner/post_list.html'
    context_object_name = 'posts'

class PostCreateView(FormView):
    template_name = 'partner/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('partner:post_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'partner/post_detail.html', {'post': post})
 
def FAQ(request):
    return render(request, 'partner/faq.html')

def signoutview(request):
    """
    Déconnecte l'utilisateur et le redirige vers la page de connexion.
    """
    auth_logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('partner:signin')

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('partner:index')  # Redirigez vers la page d'accueil ou une autre page après la mise à jour du post
    else:
        form = PostForm(instance=post)
    return render(request, 'partner/update_post.html', {'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('partner:index')  # Redirigez vers la page d'accueil ou une autre page après la suppression du post
    return render(request, 'partner/post_confirm_delete.html', {'post': post})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le post a été mis à jour avec succès.')
            return redirect('partner:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'partner/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Le post a été supprimé avec succès.')
        return redirect('partner:post_list')
    return render(request, 'partner/post_confirm_delete.html', {'post': post})

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La news a été créée avec succès.')
            return redirect('partner:news_list')
    else:
        form = NewsForm()
    return render(request, 'partner/news_form.html', {'form': form})

def news_list(request):
    news = News.objects.all()
    return render(request, 'partner/news_list.html', {'news': news})

@login_required
def news_update(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'La news a été mise à jour avec succès.')
            return redirect('partner:news_detail', pk=pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'partner/news_form.html', {'form': form})

@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'La news a été supprimée avec succès.')
        return redirect('partner:news_list')
    return render(request, 'partner/news_confirm_delete.html', {'news': news})