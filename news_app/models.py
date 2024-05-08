from django.db import models
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=100) # 標題
    url = models.URLField(max_length=1024) # 連結
    source = models.CharField(max_length=255) # 來源出處
    published_at = models.DateTimeField(null=True) #發布時間
    created_at = models.DateTimeField(auto_now_add=True) # 新增時間
    updated_at = models.DateTimeField(auto_now=True) # 更新時間
    deleted_at = models.DateTimeField(null=True) # 軟刪除
    
    def __str__(self):
        return self.title
    def delete(self):
        self.deleted_at = timezone.now()
        self.save()