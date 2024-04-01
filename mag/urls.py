from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import * 

#app_name = 'mag'

urlpatterns = [
    path('', indexView.as_view(), name="index"),
    path('signin/', Signinview.as_view(), name="signin"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signout/', signoutview, name='signout'),
    path('contact/', contact_Us , name='contact'),
    path('FAQ/', FAQ, name="FAQ"),
    path('about/', about_us , name ='about'),
    path('category_post/', category_post , name ='category_post'),
    path('category_news/', category_news , name ='category_news'),
    path('post_details/<int:id>',  post_detail, name="post_detail"),
    path('news_details/<int:id>',  news_detail, name="news_detail"),
    path('search/', search_feature, name="search_feature"),
    path('terms_of_use/', terms_of_use, name="terms_of_use"),
    path('post_detail_template/', post_detail_template, name="post_detail_template"),
    path('index_partenaire', index_partenaire, name="index_partenaire"),
    path('post_detail_template2/', post_detail_template2, name="post_detail_template2"),

]