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

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    def count_posts_in_category(category):
        return category.post_set.count()
    
class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='Media/profile_pictures/')
    date_joined = models.DateTimeField(('date joined'), auto_now=True)

    class Meta:
        unique_together = ('email',)
    
    def __str__(self):
        return self.name
    
class Post(models.Model): 
    title = models.CharField(max_length=100, unique=True) 
    slug = models.SlugField(unique=True) 
    body = models.TextField(max_length=2555) 
    pub_date = models.DateTimeField('date published', auto_now=True, )
    Category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='Media/main_images/')
    likes = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='Media/thumbnails/', null=True, blank=True)
    numberView = models.IntegerField(null=True,)

    def __str__(self):
        return self.title

    def was_seen_by_user(self, user):
        #vérifie que le poste ai été vue par un spécifique user
        return Post.objects.filter(utilisateur__user=user, post=self).exists()

    def count_views(self):
         return self.postseen_set.count()
        #Compte  le nombre de vues
        # numberView = Post.objects.filter(post=self).count()
        # return numberView
    
    def search_posts(self, query):
        return Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    
    def get_absolute_url(self):
        return reverse(" post_detail", kwargs={"pk": self.pk})
    
    
class LikePost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
class PostSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 
    body = models.TextField(max_length=255)
    birth_date = models.DateField()
    pub_date = models.DateTimeField('date published', auto_now=True, )
    Category = models.ManyToManyField(Category)
    likes = models.IntegerField(default=0)
    main_image = models.ImageField(upload_to='Media/main_images_news/')
    thumbnail = models.ImageField(upload_to='Media/thumbnails_news/', null=True, blank=True)


    def __str__(self):
        return self.title

    def was_seen_by_user(self, user):
        return News.objects.filter(user=user, news=self).exists()

    def count_views(self):
        return News.objects.filter(news=self).count()

    def search_news(self, query):
    # Use the Q object to create a complex query        posts = Post.objects.filter(
        news = News.objects.filter()
        # Q(title__icontains=query) | Q(content__icontains=query))
        return news
    
    def get_absolute_url(self):
        return reverse(" news_detail", kwargs={"pk": self.pk})
    
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

class post_image(models.Model):
    image=models.ImageField()
    Post=models.ForeignKey(Post, on_delete=models.CASCADE)

    #Pensez à créer la class Result pour les résultats des différents events 