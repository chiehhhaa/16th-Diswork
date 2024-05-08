from django.urls import path
from .views import NewsSearchView

app_name = "news"

urlpatterns = [
    path("news/", NewsSearchView.as_view(), name="news_search"),
]
