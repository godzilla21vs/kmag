from django.urls import path
from .views import (
    index,
    SigninView,
    contact_Us,
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    NewsListView,
    NewsCreateView,
    NewsDetailView,
    NewsUpdateView,
    NewsDeleteView,
    FAQ,
    profile,
)

app_name = 'partner'

urlpatterns = [
    path('partner/posts/', PostListView.as_view(), name='post_list'),
    path('partner/posts/create/', PostCreateView.as_view(), name='post_create'),
    path('partner/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('partner/posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('partner/posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('partner/news/', NewsListView.as_view(), name='news_list'),
    path('partner/news/create/', NewsCreateView.as_view(), name='news_create'),
    path('partner/news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('partner/news/<int:pk>/update/', NewsUpdateView.as_view(), name='news_update'),
    path('partner/news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('partner/contact/', contact_Us, name='contact'),
    path('partner/signin/', SigninView.as_view(), name="signin"),
    path('partner/FAQ/', FAQ, name="FAQ"),
    path('partner/profile/', profile, name='profile'),
    path('partner/', index, name="index"),
]
