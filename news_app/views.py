# from django.views.generic import TemplateView
# from bs4 import BeautifulSoup
# import requests

# class NewsSearchView(TemplateView):
#     template_name = "news.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         url = "https://tw.news.yahoo.com/archive/"
#         response = requests.get(url)
#         data = BeautifulSoup(response.text, "html.parser")
#         titles = data.find_all("h3", class_="Mb(5px)")
#         news_items = []
#         for title in titles:
#             news_link = title.find("a", href=True)
#             if news_link:
#                 full_url = news_link["href"]
#                 if not full_url.startswith("https"):
#                     full_url = url + full_url
                    
#                 # 來源出處
#                 source = requests.get(full_url)
#                 source_data = BeautifulSoup(source.text, "html.parser")
#                 source_name_tag = source_data.find("div", class_="source-info")
#                 if source_name_tag:
#                     source_name = source_name_tag.text.strip()
#                 else:
#                     source_name = "出處不明！"
                
#                 # 加入要顯示的內容
#                 news_items.append({
#                     "text": title.text.strip(),
#                     "url": full_url,
#                     "source":source_name,
#                 }) 
#         context['news_items'] = news_items
#         return context




# from django.views.generic import TemplateView
# from bs4 import BeautifulSoup
# import requests
# from django.core.paginator import Paginator

# class NewsSearchView(TemplateView):
#     template_name = "news.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         page = self.request.GET.get('page', 1)  # 從GET請求中獲取頁面數，默認為第一頁
#         url = "https://tw.news.yahoo.com/archive/"
#         response = requests.get(url)
#         data = BeautifulSoup(response.text, "html.parser")
#         titles = data.find_all("h3", class_="Mb(5px)")
#         news_items = []

#         for title in titles:
#             news_url = title.find("a", href=True)
#             if news_url:
#                 full_url = news_url["href"]
#                 if not full_url.startswith("https"):
#                     full_url = url + full_url

#                 source = requests.get(full_url)
#                 source_data = BeautifulSoup(source.text, "html.parser")
#                 source_name_tag = source_data.find("div", class_="source-info")
#                 source_name = source_name_tag.text.strip() if source_name_tag else "出處不明！"
                
#                 news_items.append({
#                     "text": title.text.strip(),
#                     "url": full_url,
#                     "source": source_name,
#                 })
#         # 使用Paginator
#         paginator = Paginator(news_items, 5)  # 每頁5筆數據
#         page_obj = paginator.get_page(page)  # 獲取當前頁面的數據
#         context['page_obj'] = page_obj
#         return context








from django.views.generic import ListView
from django.shortcuts import redirect
from .models import News
import requests
from bs4 import BeautifulSoup

class NewsSearchView(ListView):
    model = News
    template_name = "news.html"
    context_object_name = 'news_items'
    paginate_by = 5
    
    def get_queryset(self):
        self.update_news()
        return News.objects.all().order_by("-created_at")

    def update_news(self):
        url = "https://tw.news.yahoo.com/archive/"
        response = requests.get(url)
        data = BeautifulSoup(response.text, "html.parser")
        titles = data.find_all("h3", class_="Mb(5px)")

        for title in titles:
            news_url = title.find("a", href=True)
            if news_url:
                full_url = news_url["href"]
                if not full_url.startswith("https"):
                    full_url = url + full_url

                if not News.objects.filter(url=full_url).exists():
                    source = requests.get(full_url)
                    source_data = BeautifulSoup(source.text, "html.parser")
                    source_name_tag = source_data.find("div", class_="source-info")
                    source_name = source_name_tag.text.strip() if source_name_tag else "出處不明！"
                    # 儲存進資料庫
                    News.objects.create(
                        title=title.text.strip(),
                        url=full_url,
                        source=source_name
                    )
