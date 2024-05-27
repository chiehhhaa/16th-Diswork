from django.contrib import admin
from django.urls import path, include
from .views import IndexView, PremiumView, custom_page_not_found_view
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404



urlpatterns = [
    path("", IndexView.as_view(), name="root"),
    path("premium/", PremiumView.as_view(), name="premium"),
    path("members/", include("members.urls")),
    path("friends/", include("friends.urls")),
    path("events/", include("events.urls")),
    path("news/", include("news.urls")),
    path("chat/", include("chats.urls")),
    path("tasks/", include("tasks.urls")),
    path("boards/", include("boards.urls")),
    path("accounts/", include("allauth.urls")),
    path("comments/", include("comments.urls")),
    path("articles/", include("articles.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_page_not_found_view