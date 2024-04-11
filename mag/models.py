import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify

# Création des modèles

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Utilisateur')
    GENDER_CHOICES = (
        ('H', 'HOMME'),
        ('F', 'FEMME'),
        ('A', 'AUTRE')
    )
    genre = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    mobile = models.PositiveIntegerField(null=True, blank=True)
    adresse = models.CharField(max_length=500, null=True, blank=True)
    ville = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username

class ProfilePicture(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/profile_pictures/')

class Post(models.Model): 
    title = models.CharField(max_length=100, unique=True) 
    slug = models.SlugField(unique=True) 
    body = models.TextField(max_length=2995) 
    pub_date = models.DateTimeField('date published', auto_now=True, )
    Category = models.ForeignKey('Category', on_delete=models.CASCADE) 
    Author = models.ForeignKey('Author', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    numberView = models.IntegerField(null=True,)

    def __str__(self):
        return self.title

    def was_seen_by_user(self, user):
        return Post.objects.filter(utilisateur__user=user, post=self).exists()

    def count_views(self):
         return self.postseen_set.count()
    
    def search_posts(self, query):
        return Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    
    def get_absolute_url(self):
        return reverse(" post_detail", kwargs={"pk": self.pk})
    
class MainImage(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/main_images/')

class Thumbnail(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/thumbnails/', null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    date_joined = models.DateTimeField(('date joined'), auto_now=True)

    class Meta:
        unique_together = ('email',)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commenté par {self.author.username} on {self.post.title} at {self.created_at}"

class PostSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']
    
class LikePost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 
    body = models.TextField(max_length=2955)
    pub_date = models.DateTimeField('date published', auto_now=True,)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    numberView = models.IntegerField(null=True,)

    def __str__(self):
        return self.title

    def was_seen_by_user(self, user):
        return News.objects.filter(user=user, news=self).exists()

    def count_views(self):
        return News.objects.filter(news=self).count()

    def search_news(self, query):
        return News.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    def get_absolute_url(self):
        return reverse(" news_detail", kwargs={"pk": self.pk})

class CommentNews(models.Model):
    news = models.ForeignKey('News', related_name='commentsNews', on_delete=models.CASCADE)
    author = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commenté par {self.author.username} on {self.news.title} at {self.created_at}"

class LikeNews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class newsSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'news']

class Subscriber(models.Model):
    email= models.EmailField(unique=True)

    def __str__(self):
        return self.email
class MainImageNews(models.Model):
    News = models.OneToOneField(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/main_images_news/')

class ThumbnailNews(models.Model):
    News = models.OneToOneField(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/thumbnails_news/', null=True, blank=True)

class post_image(models.Model):
    image=models.ImageField()
    Post=models.ForeignKey(Post, on_delete=models.CASCADE)
