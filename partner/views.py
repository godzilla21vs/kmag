from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, News
from .forms import PostForm, NewsForm

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

# Les autres vues CRUD pour les posts (update, delete) seront similaires à post_create.

def news_list(request):
    news = News.objects.all()
    return render(request, 'news_list.html', {'news': news})

# Les autres vues CRUD pour les news seront similaires à celles des posts.
