from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import * 
from . import views
from django.conf import settings

app_name = 'mag'

urlpatterns = [
    path('', indexView.as_view(), name='index'),
    path('signin/', SigninView.as_view(), name="signin"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signout/', signoutview, name='signout'),
    path('contact/', contact_Us , name='contact'),
    path('FAQ/', FAQ, name="FAQ"),
    path('about/', about_us , name ='about'),
    path('post_details/<int:pk>',  post_detail, name="post_detail"),
    path('news_details/<int:pk>',  news_detail, name="news_detail"),
    path('search/', search_feature, name="search_feature"),
    path('terms_of_use/', terms_of_use, name="terms_of_use"),
    path('post_detail_template/', post_detail_template, name="post_detail_template"),
    # path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('profile/', ProfileView, name='profile'),
    path('category/<str:category_name>', category, name="category"),
    path('indexpartner/<str:author_name>/', indexpartner, name="indexpartner"),
    path('like/', views.like, name='like'),
]
