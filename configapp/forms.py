from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "avatar", "website"]



class UserLoginForm(forms.Form):
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    password = forms.CharField(label='parol', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}))

    class Meta:
        fields = ['username', 'password']