from .models import Friend, Card
from members.models import Member
from boards.models import Category
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.views import View
from django.views.generic import ListView, DeleteView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from lib.paginate_que import paginate_queryset
import random


@method_decorator(login_required, name="dispatch")
class MemberListView(ListView):
    model = Member
    template_name = "friends/search_list.html"
    context_object_name = "search_list"
    paginate_by = 5

    def get_queryset(self):
        query = super().get_queryset().exclude(username=self.request.user)
        keyword = self.request.GET.get("username", "").strip()
        if keyword:
            return query.filter(username__icontains=keyword)
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context
    

@method_decorator(login_required, name="dispatch")
class FriendListView(ListView):
    model = Friend
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(sender=user, status="2") | Friend.objects.filter(
            receiver=user, status="2"
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context


@method_decorator(login_required, name="dispatch")
class FriendDeleteView(DeleteView):
    model = Friend
    template_name = "friends/confirm_delete.html"
    success_url = reverse_lazy("friends:friend_list")    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all()
        return context


@login_required
def send_friend_request(req, receiver_id):
    try:
        receiver_id = int(receiver_id)
    except ValueError:
        messages.error(req, "無效的接收者ID")
        return redirect("friends:member_list")

    sender_id = req.user.id
    receiver_exists = Member.objects.filter(id=receiver_id).exists()

    if req.method == "POST":
        is_friend = Friend.objects.filter(Q(sender_id=sender_id, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver_id=sender_id)).exists()
        friend = Friend.objects.filter(Q(sender_id=sender_id, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver_id=sender_id)).first()
        if is_friend:
            if friend.status == "2":
                messages.error(req, "己經是好友了。")
            elif friend.receiver_id == req.user.id:
                messages.error(req, "對方己發送好友通知，請到等待中加好友！")        
            else:    
                messages.error(req, "好友邀請已經發送過了！")
        else:
            messages.success(req, "好友邀請已發送！")
            Friend.objects.create(sender_id=sender_id, receiver_id=receiver_id)
        return redirect("friends:member_list")
    else:
        messages.error(req, "操作錯誤！")
        return redirect("friends:member_list")

@login_required
def accept_friend_request(req, friend_request_id):
    members = Member.objects.exclude(id=req.user.id)
    page_number = req.POST.get("page")
    page_obj, is_paginated  = paginate_queryset(members, page_number, 5)
    
    if req.method == "POST":
        friend_request_exists = Friend.objects.filter(id=friend_request_id).exists()
        friend_request = Friend.objects.filter(id=friend_request_id).first()
        if not friend_request_exists:
            messages.error(req, "沒有這筆加好友資料!")

        if friend_request.status == "1":
            friend_request.status = "2"
            friend_request.save()
            messages.success(req, "好友邀請已接受。")
        else:
            messages.error(req, "發送好友狀態代號不對。")    
    else:
        messages.error(req, "操作錯誤！")    

    redirect_url = reverse("friends:member_list")
    if is_paginated:
        redirect_url += f"?page={page_number}"

    return redirect(redirect_url)    


@login_required
def reject_friend_request(req, friend_request_id):
    members = Member.objects.exclude(id=req.user.id)
    page_number = req.POST.get("page")
    page_obj, is_paginated  = paginate_queryset(members, page_number, 5)
    print("reject", friend_request_id)
    if req.method == "POST":
        friend_request_exists = Friend.objects.filter(id=friend_request_id).exists()
        friend_request = Friend.objects.filter(id=friend_request_id).first()
        if not friend_request_exists:
            messages.error(req, "沒有這筆資料！")

        if friend_request.status == "1":
            friend_request.status = "3"
            friend_request.save()
            messages.success(req, "拒絕加入好友！")
        else:
            messages.error(req, "發送好友狀態代號不對。")      
    else:
        messages.error(req, "操作錯誤！")
    redirect_url = reverse("friends:member_list")
    if is_paginated:
        redirect_url += f"?page={page_number}"

    return redirect(redirect_url)   


@login_required
def friend_requests(req):
    received_requests = Friend.objects.filter(receiver=req.user, status="1")
    category_list = Category.objects.all()

    return render(
        req, "friends/friend_requests.html", {"received_requests": received_requests, "category_list": category_list}
    )


class DrawCardView(View):
    def get_queryset(self, user):
        friends = Friend.objects.filter(
            Q(sender=user, status="2") | Q(receiver=user, status="2")
        )

        friend_ids = set()
        for friend in friends:
            if friend.sender == user:
                friend_ids.add(friend.receiver.id)
            elif friend.receiver == user:
                friend_ids.add(friend.sender.id)

        return Member.objects.exclude(id__in=friend_ids).exclude(id=user.id)

    def get(self, request):
        user = request.user
        members = list(self.get_queryset(user))
        today = timezone.now().date()
        category_list = Category.objects.all()

        already_drew_today = (
            Card.objects.annotate(date=TruncDate("created_at"))
            .filter(drawer=user)
            .first()
        )

        if already_drew_today:
            random_member = already_drew_today.drawn
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                member_data = {
                    "id": random_member.id,
                    "username": random_member.username,
                    "name": random_member.name or "未填寫",
                    "user_img": (
                        random_member.user_img.url
                        if random_member.user_img
                        else "/static/image/cathead.png"
                    ),
                    "birthday": (
                        random_member.birthday.strftime("%Y-%m-%d")
                        if random_member.birthday
                        else "未填寫"
                    ),
                    "interest": random_member.interest or "未填寫",
                    "constellation": random_member.constellation or "未填寫",
                }
                return JsonResponse(member_data)
            else:
                return render(
                    request,
                    "friends/card.html",
                    {"drawn_member": random_member, "draw_limit_reached": True, "category_list": category_list},
                )

        random_member = None

        random_member = random.choice(members)
        existing_card = Card.objects.filter(drawer=user, drawn=random_member).exists()

        card = Card.objects.create(drawer=user, drawn=random_member)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            member_data = {
                "id": random_member.id,
                "username": random_member.username,
                "name": random_member.name or "未填寫",
                "user_img": (
                    random_member.user_img.url
                    if random_member.user_img
                    else "/static/image/cathead.png"
                ),
                "birthday": (
                    random_member.birthday.strftime("%Y-%m-%d")
                    if random_member.birthday
                    else "未填寫"
                ),
                "interest": random_member.interest or "未填寫",
                "constellation": random_member.constellation or "未填寫",
            }
            return JsonResponse(member_data)
        else:
            return render(request, "friends/card.html", {"drawn_member": random_member, "category_list": category_list})
