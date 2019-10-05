from django import forms
from django.contrib.auth.models import User
from .models import Recruitment, ApplicantModel


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "text", "style": "background-color: transparent", "placeholder": "账号",
                       "onfocus": "this.value=''"}),
            "password": forms.PasswordInput(
                attrs={"class": "password", "style": "background-color: transparent", "placeholder": "密码",
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
                attrs={"class": "text", "style": "background-color: transparent", "placeholder": "账号",
                       "onfocus": "this.value=''"}),
            "password": forms.PasswordInput(
                attrs={"class": "password", "style": "background-color: transparent", "placeholder": "密码",
                       "onfocus": "this.value=''"}),
            "email": forms.EmailInput(
                attrs={"class": "email", "style": "background-color: transparent", "placeholder": "邮箱"}),

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


class ModifyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {

            "password": forms.PasswordInput(
                attrs={"class": "password", "style": "background-color: transparent", "placeholder": "密码",
                       "onfocus": "this.value=''"}),
            "email": forms.EmailInput(
                attrs={"class": "email", "style": "background-color: transparent", "placeholder": "邮箱"}),

        }
        labels = {
            "password": '',
            "email": '',

        }

        help_texts = {
            "password": '',
            "email": ''
        }


class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        exclude = ['release_time', 'create_time']


class AppliactionForm(forms.ModelForm):
    class Meta:
        model = ApplicantModel
        exclude = ["uid"]
