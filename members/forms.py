from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Member


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        label="姓名",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    email = forms.EmailField(
        label="信箱",
        widget=forms.EmailInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )

    class Meta:
        model = Member
        fields = ("name", "username", "email", "password1", "password2")


class MemberUpdateForm(UserChangeForm):
    name = forms.CharField(
        label="姓名：",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    username = forms.CharField(
        label="帳號：",
        widget=forms.TextInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    email = forms.EmailField(
        label="信箱：",
        widget=forms.EmailInput(attrs={"class": "mx-1 border-2 border-gray-300"}),
    )
    password = None

    class Meta:
        model = Member
        fields = ("name", "username", "email")
