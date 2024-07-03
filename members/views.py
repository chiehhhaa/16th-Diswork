from .forms import SignUpForm, MemberUpdateForm
from .models import Member
from boards.models import Category
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, UpdateView, DetailView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import login, logout, get_backends
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from dotenv import load_dotenv
import os

load_dotenv()


@login_required
def subscribe(request):
    user = request.user
    member = Member.objects.get(username=user.username)
    if request.method == "POST":
        if member.member_status == "1":
            return render(request, "pages/index.html", {"member_status": True})
        else:
            member.member_status = "1"
            member.save()
            return render(request, "pages/index.html", {"member_status": True})
    else:
        return render(
            request, "pages/index.html", {"member_status": member.member_status == "1"}
        )


class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("root")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(TemplateView):
    template_name = "registration/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("root")


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy("members:login")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        if Member.objects.filter(email=email).exists():
            messages.error(self.request, "此電子郵件已被註冊！！！")
            return self.form_invalid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = self.request.build_absolute_uri(
            reverse("members:activate", kwargs={"uidb64": uid, "token": token})
        )

        send_mail(
            "Diswork會員驗證信件",
            "點擊此連結驗證您的帳戶：{}".format(link),
            os.getenv("DEFAULT_FROM_EMAIL"),
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, "請至您的註冊信箱查看信件並完成註冊。")
        return super().form_valid(form)


class ProfileView(DetailView):
    model = Member
    form_class = MemberUpdateForm
    template_name = "registration/profile.html"
    context_object_name = "member"

    def get_object(self, queryset=None):
        obj = super(ProfileView, self).get_object(queryset=queryset)
        if obj != self.request.user:
            raise PermissionDenied()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context


@method_decorator(login_required, name="dispatch")
class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberUpdateForm
    template_name = "registration/edit.html"
    context_object_name = "member"

    def get_success_url(self):
        return reverse_lazy("members:profile", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        obj = Member.objects.get(pk=pk)
        if obj != self.request.user:
            raise PermissionDenied()
        return obj

    def for_valid(self, form):
        member = form.save(commit=False)
        if not form.cleaned_data["user_img"]:
            member.user_img = self.get_object().user_img
        member.save()
        return super().form_valid(form)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        backends = get_backends()
        if backends:
            user.backend = "{}.{}".format(
                backends[0].__module__, backends[0].__class__.__name__
            )
        login(request, user)
        messages.success(request, "您的帳號已驗證成功！")
        return redirect("members:login")
    else:
        messages.error(request, "驗證連結無效！")
        return redirect("members:register")
