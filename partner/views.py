from django.http import request
from django.http import HttpRequest
from django.views.generic import TemplateView, FormView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.shortcuts import redirect
from django.urls import reverse
from mag.models import *
from mag.forms import *
from django.shortcuts import get_object_or_404

# if request.user.is_authenticated:
#     username = request.user.username
    
class IndexView(TemplateView):
    template_name = 'partner/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = 2024
        return context

class SigninView(FormView):
    template_name = 'partner/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('partner:index')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Vous êtes maintenant connecté.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Veuillez vérifier vos informations de connexion.")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Vous êtes déjà authentifié. Redirection...")
            return redirect(reverse('partner:index'))
        return super().dispatch(request, *args, **kwargs)

class SignoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
        return redirect('partner:signin')

class ContactUsView(TemplateView):
    template_name = 'partner/contact_us.html'

class FAQView(TemplateView):
    template_name = 'partner/faq.html'

class ProfileView(TemplateView):
    template_name = 'partner/profile.html'

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'partner/post_list.html'
    context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, FormView):
    template_name = 'partner/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('partner:post_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Le post a été créé avec succès.')
        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'partner/post_detail.html'

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'partner/post_form.html'

    def get_success_url(self):
        return reverse_lazy('partner:post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'partner/post_confirm_delete.html'
    success_url = reverse_lazy('partner:post_list')

class NewsCreateView(LoginRequiredMixin, FormView):
    template_name = 'partner/news_form.html'
    form_class = NewsForm
    success_url = reverse_lazy('partner:news_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'La news a été créée avec succès.')
        return super().form_valid(form)

class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'partner/news_list.html'
    context_object_name = 'news'

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'partner/news_form.html'

    def get_success_url(self):
        return reverse_lazy('partner:news_detail', kwargs={'pk': self.object.pk})

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'partner/news_confirm_delete.html'
    success_url = reverse_lazy('partner:news_list')

class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'partner/news_detail.html'
