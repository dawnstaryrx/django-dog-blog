from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .feeds import AllArticlesFeed

urlpatterns = [
    path("", views.home, name = "home-page"),
    path("posts/", views.posts, name = "posts-page"),
    path("categories/", views.categories, name = "categories-page"),
    # article
    path("write/", views.write, name = "write-page"),
    path("article/<str:pk>", views.article_detail, name = "article-detail"),
    path("article/update/<str:pk>", views.article_update, name = "article-update"),
    path("article/delete/<str:pk>", views.article_delete, name = "article-delete"),
    path("article/download/<str:pk>", views.article_download, name = "article-download"),
    # category
    path("categories/create/", views.create_category, name = "create-category"),
    path("categories/update/<str:pk>/", views.update_category, name = "update-category"),
    path("categories/delete/<str:pk>/", views.delete_category, name = "delete-category"),
    # tag
    path("tag/create/", views.create_tag, name = "create-tag"),
    path("tag/update/<str:pk>/", views.update_tag, name = "update-tag"),
    path("tag/delete/<str:pk>/", views.delete_tag, name = "delete-tag"),
    # login logout
    path("login/", views.login_page, name="login-page"),
    path("logout/", views.logout_page, name="logout-page"),
    # picture
    path("picture/", views.picture_page, name="picture-page"),
    path("picture/upload/", views.upload_picture, name="picture-upload"),
    # 添加 RSS Feed URL
    path('rss/all/', AllArticlesFeed(), name='all_articles_feed'),
    
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
handler404 = views.page_not_found 
handler500 = views.internet_server_error