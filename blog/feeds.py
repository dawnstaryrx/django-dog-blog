# blog/feeds.py
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from .models import Article

class AllArticlesFeed(Feed):
    title = "所有文章"
    link = "/rss/all/"
    description = "本站发布的所有文章。"

    def items(self):
        # 获取所有已发布的文章，按发布时间降序排列
        return Article.objects.filter(status='p').order_by('-published')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # 可根据需要调整截取的单词数
        return truncatewords(item.content, 50)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published
