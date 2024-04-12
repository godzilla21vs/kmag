from django.urls import path
from .views import *

app_name = 'partner'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/update/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('signin/', SigninView.as_view(), name="signin"),
    path('FAQ/', FAQView.as_view(), name="FAQ"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', IndexView.as_view(), name="index"),
]
