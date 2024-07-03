from .models import Category
from members.models import Member
from .forms import CategoryForm
from django.views.generic import ListView, FormView, DetailView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@method_decorator(login_required, name="dispatch")
class BoardIndexView(ListView):
    model = Category
    template_name = "boards/board_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword", "").strip()
        if keyword:
            queryset = queryset.filter(tittle__icontains=keyword)
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                member = Member.objects.get(username=self.request.user.username)
                context["member_status"] = member.member_status
            except Member.DoesNotExist:
                context["member_status"] = "0"
        else:
            context["member_status"] = "0"
        return context


@method_decorator(login_required, name="dispatch")
class BoardDetailView(DetailView):
    model = Category
    template_name = "boards/board_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword", "").strip()
        return queryset.filter(title__icontains=keyword)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name="dispatch")
class BoardNewView(FormView):
    model = Category
    form_class = CategoryForm
    template_name = "boards/new.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        try:
            member = Member.objects.get(username=user.username)
        except Member.DoesNotExist:
            raise PermissionDenied()
        if member.member_status != "1":
            return render(request, "403.html", {"member_status": False})
        return super(BoardNewView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context


@login_required
@require_POST
def create(req):
    form = CategoryForm(req.POST, req.FILES)
    if form.is_valid():
        category = form.save(commit=False)
        category.member_id = req.user.id
        category.save()
    return redirect("boards:list")


@method_decorator(login_required, name="dispatch")
class BoardUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "boards/edit.html"

    def get_success_url(self):
        return reverse_lazy("boards:list")

    def get_object(self, queryset=None):
        obj = super(BoardUpdateView, self).get_object(queryset=queryset)
        if obj.member.id != self.request.user.id:
            raise PermissionDenied()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context


@method_decorator(login_required, name="dispatch")
class BoardDeleteView(DeleteView):
    model = Category

    def get_success_url(self):
        return reverse_lazy("boards:list")
