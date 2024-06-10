from django.contrib import admin
from .models import Category, Tag, Article, Picture
# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)


class PictureAdmin(admin.ModelAdmin):
  list_display=('name', 'img')
admin.site.register(Picture, PictureAdmin)