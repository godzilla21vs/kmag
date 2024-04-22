from django.http import request
from django.http import HttpRequest
from django.views.generic import TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.shortcuts import redirect, render
from django.urls import reverse
from mag.models import *
from mag.forms import *
from django.shortcuts import get_object_or_404

# if request.user.is_authenticated:
#     username = request.user.username

class SigninAuthorView(View):
    def get(self, request):
        form = SigninAuthorForm()
        return render(request, 'partner/login.html', {'form': form})

    def post(self, request):
        form = SigninAuthorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            author = authenticate(request, name=name, password=password)
            if author:
                login(request, author)
                context = {'form': form, 'author_name': author.name}
                return redirect('partner:home')  # Remplacez 'home' par l'URL de la page à laquelle vous souhaitez rediriger après la connexion
        return render(request, 'partner/login.html', context)
    
@login_required    
class IndexView(TemplateView):
    template_name = 'partner/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = 2024
        # Récupérer le nom de l'auteur du contexte de la requête
        context['author_name'] = self.request.user.name
        return context


@login_required
class SignoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
        return redirect('partner:logout')

@login_required
class ContactUsView(TemplateView):
    template_name = 'partner/contact_us.html'

@login_required
class FAQView(TemplateView):
    template_name = 'partner/faq.html'

@login_required
class LogoutView(TemplateView):
    template_name = 'partner/logout.html'

class ProfileView(TemplateView):
    template_name = 'partner/profile.html'

@login_required
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'partner/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        author = get_object_or_404(Author, name=self.request.user.name)
        return Post.objects.filter(Author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(Author, name=self.request.user.name)
        context['author'] = author
        return context

@login_required
class PostCreateView(LoginRequiredMixin, FormView):
    template_name = 'partner/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('partner:post_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Le post a été créé avec succès.')
        return super().form_valid(form)

@login_required
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'partner/post_detail.html'

@login_required
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'partner/post_form.html'

    def get_success_url(self):
        return reverse_lazy('partner:post_detail', kwargs={'pk': self.object.pk})

@login_required
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'partner/post_confirm_delete.html'
    success_url = reverse_lazy('partner:post_list')

@login_required
class NewsCreateView(LoginRequiredMixin, FormView):
    template_name = 'partner/news_form.html'
    form_class = NewsForm
    success_url = reverse_lazy('partner:news_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'La news a été créée avec succès.')
        return super().form_valid(form)

@login_required
class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'partner/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        author = get_object_or_404(Author, name=self.request.user.name)
        return News.objects.filter(Author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(Author, name=self.request.user.name)
        context['author'] = author
        return context


@login_required
class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'partner/news_form.html'

    def get_success_url(self):
        return reverse_lazy('partner:news_detail', kwargs={'pk': self.object.pk})

@login_required
class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'partner/news_confirm_delete.html'
    success_url = reverse_lazy('partner:news_list')

@login_required
class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'partner/news_detail.html'
