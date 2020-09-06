from .models import CustomUser,Post,Comment,Like
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1")
        model = CustomUser

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_banner','title','text',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'postcontent'}), }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})}
