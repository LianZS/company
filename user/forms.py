from django import forms
from django.contrib.auth.models import User


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
        # error_messages = {
        #     "username": {
        #         "max_length": "This writer's name is too long",
        #
        #     },
        #     "password": {
        #         "max_length": "This writer's name is too long",
        #
        #     }
        # }
        help_texts = {
            "username": '',
            "password": ''
        }
