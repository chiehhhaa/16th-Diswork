from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect


# 登入
class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


# 登出
class LogoutView(TemplateView):
    template_name = "registration/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "登出成功！")
        return redirect("index")


# 註冊
class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy("members:login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "註冊成功！")
        return super().form_valid(form)
