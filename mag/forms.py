from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cette adresse e-mail est déjà associée à un compte. Veuillez utiliser une autre adresse e-mail.')
        return email


class CustomAuthenticationForm(AuthenticationForm):
    pass

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('genre', 'adresse', 'mobile', 'ville',)

class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmer mot de passe', widget=forms.PasswordInput)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'Category', 'Author', 'main_image', 'thumbnail']

        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields['Category'].queryset = Category.objects.all()

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