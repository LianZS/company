from django import forms


class LoginForm(forms.Form):
    user_name = forms.CharField(label="帐户名", max_length=100)
    user_password = forms.CharField(label="密码", max_length=100,widget=forms.PasswordInput)
