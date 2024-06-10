from django.db import models
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    name = models.CharField('分类名称', max_length=50)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated']
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField('名称', max_length=20)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated']
        verbose_name = "标签"
        verbose_name_plural = verbose_name
    

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )

    title = models.CharField('标题', max_length=50)
    content = models.TextField('正文', null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="类别", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签集合', blank=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField('浏览量', default=0)
    published = models.DateTimeField('发布时间', default= now, null=True)
    updated = models.DateTimeField('更新时间',  auto_now=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title
    
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-published']
        verbose_name = "文章"
        verbose_name_plural = verbose_name