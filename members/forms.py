from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="帳號", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    email = forms.EmailField(
        label="電子郵件", widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    password1 = forms.CharField(
        label="密碼", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="密碼確認", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
