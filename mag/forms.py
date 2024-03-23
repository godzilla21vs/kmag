from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('last_name','first_name', 'email', 'password1', 'password2')


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('genre', 'adresse', 'mobile', 'ville',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'Category', 'Author', 'main_image', 'thumbnail']

        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields['Category'].queryset = Category.objects.all()
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        #     'slug': forms.TextInput(attrs={'class': 'form-control'}),
        #     'body': forms.Textarea(attrs={'class': 'form-control'}),
        #     'Category': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        #     'Author': forms.Select(attrs={'class': 'form-control'}),
        #     'main_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        #     'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        # }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'body', 'Category', 'main_image', 'thumbnail']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
#         widgets = {
#             'name': forms.CharField(attrs={'class': 'form-control'}),
#             'slug': forms.TextInput(attrs={'class': 'form-control'})

#         }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'email']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailField(attrs={'class': 'form-control'})
#         }

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)
#         widgets = {
#             'email': forms.EmailField(attrs={'class': 'form-control'}),
#         }