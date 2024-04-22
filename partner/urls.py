from django.urls import path
from .views import *

app_name = 'partner'

urlpatterns = [
    path('posts/', PostListView, name='post_list'),
    path('posts/create/', PostCreateView, name='post_create'),
    path('posts/<int:pk>/', PostDetailView, name='post_detail'),
    path('posts/<int:pk>/update/', PostUpdateView, name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView, name='post_delete'),
    path('news/', NewsListView, name='news_list'),
    path('news/create/', NewsCreateView, name='news_create'),
    path('news/<int:pk>/', NewsDetailView, name='news_detail'),
    path('news/<int:pk>/update/', NewsUpdateView, name='news_update'),
    path('news/<int:pk>/delete/', NewsDeleteView, name='news_delete'),
    path('contact/', ContactUsView, name='contact'),
    path('', SigninAuthorView.as_view(), name="signin"),
    path('FAQ/', FAQView, name="FAQ"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('home/', IndexView, name="index"),
    path('logout/', LogoutView, name="logout"),

]
