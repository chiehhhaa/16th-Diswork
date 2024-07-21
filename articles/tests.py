from django.test import TestCase
from .models import Article, LikeArticle
from members.models import Member
from comments.models import Comment
from boards.models import Category
from django.utils import timezone

class ArticleManagerTestCase(TestCase):
    def setUp(self):
        self.user1 = Member.objects.create(username='user1', email='user1@example.com')
        self.user2 = Member.objects.create(username='user2', email='user2@example.com')
        self.user3 = Member.objects.create(username='user3', email='user3@example.com')

        self.category1 = Category.objects.create(title='Category 1')
        self.category2 = Category.objects.create(title='Category 2')
        self.category3 = Category.objects.create(title='Category 3')

        self.article1 = Article.objects.create(title="Article 1", content="Content 1", author=self.user1, category=self.category1, deleted_at=None)
        self.article2 = Article.objects.create(title="Article 2", content="Content 2", author=self.user2, category=self.category2, deleted_at=timezone.now())
        self.article3 = Article.objects.create(title="Article 3", content="Content 3", category=self.category3, author=self.user3, deleted_at=None)

        # LikeArticle.objects.create(like_article=self.article1, like_by_article=self.user1)
        # LikeArticle.objects.create(like_article=self.article1, like_by_article=self.user2)
        # LikeArticle.objects.create(like_article=self.article3, like_by_article=self.user3)

        self.article1.like_article.add(self.user1)
        self.article1.like_article.add(self.user2)
        self.article3.like_article.add(self.user3)

        Comment.objects.create(member=self.user1, article=self.article1, content="Content 1")
        Comment.objects.create(member=self.user2, article=self.article3, content="Content 2")
        Comment.objects.create(member=self.user3, article=self.article3, content="Content 3", deleted_at=timezone.now())

    # def test_get_queryset(self):
    #     queryset = Article.objects.all()
    #     self.assertEqual(queryset.count(), 2) # 預期包含2筆文章，因為有1筆已經被軟刪除。
    #     self.assertNotIn(self.article2, queryset) # 確認 self.article2 不在 queryset 中，因為它已經被軟刪除。

    def test_with_count(self):
        queryset = Article.objects.with_count()
        # 從查詢集( queryset )中取得特定的文章
        article1 = queryset.get(id=self.article1.id)
        article3 = queryset.get(id=self.article3.id)


        self.assertEqual(article1.like_count, 2)  # 預期文章1會有2個喜歡者
        self.assertEqual(article3.like_count, 1)  # 預期文章3會有1個喜歡者

        self.assertEqual(article1.comment_count, 1)  # 預期文章1會有1個留言
        self.assertEqual(article3.comment_count, 1)  # 預期文章3會有1個留言（有一個留言已被軟刪除）
