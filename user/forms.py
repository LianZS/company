from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "text", "style": "background-color: transparent", "value": "账号",
                       "onfocus": "this.value=''"}),
            "password": forms.PasswordInput(
                attrs={"class": "password", "style": "background-color: transparent", "value": "密码",
                       "onfocus": "this.value=''"}),
        }
        labels = {
            "username": '',
            "password": ''
        }

        help_texts = {
            "username": '',
            "password": ''
        }


class RegisterForm(forms.ModelForm):


    class Meta:
        model = User

        fields = ['email', 'username', 'password']
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "text", "style": "background-color: transparent", "value": "账号",
                       "onfocus": "this.value=''"}),
            "password": forms.PasswordInput(
                attrs={"class": "password", "style": "background-color: transparent", "value": "密码",
                       "onfocus": "this.value=''"}),
            "email": forms.EmailInput(
                attrs={"class": "email", "style": "background-color: transparent", "value": "邮箱",
                       "onfocus": "this.value=''"}),

        }
        labels = {
            "username": '',
            "password": '',
            "email": '',

        }

        help_texts = {
            "username": '',
            "password": '',
            "email": ''
        }
