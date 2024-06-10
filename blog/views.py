from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CategoryForm, TagForm, ArticleForm, PictureForm
from .models import Category, Tag, Article, Picture
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown
from django.db.models import Q
import tempfile
from django.http import FileResponse
from django.utils.encoding import escape_uri_path


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home-page")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "用户不存在。")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, "用户名或密码错误。")
    context = {}
    return render(request, "form/login.html", context)


def logout_page(request):
    logout(request)
    return redirect('home-page')


def home(request):
    article = Article()
    try:
        article = Article.objects.get(title='home')
    except:
        article.title = "home"
        article.content = ""
    article.content = markdown.markdown(article.content,
        extensions=[
        'markdown.extensions.fenced_code',
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        'markdown.extensions.tables',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 自动生成目录
        'markdown.extensions.toc',
        ])
    context = {"article": article}
    return render(request, 'home.html', context)

def posts(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    c = request.GET.get('c') if request.GET.get('c') != None else ''
    t = request.GET.get('t') if request.GET.get('t') != None else ''
    if request.user.is_authenticated:
        if t != "" and t != None:
            articles = Article.objects.all().filter(
                Q(title__icontains = q) |
                Q(content__icontains = q) |
                Q(category__name__icontains = q)
            ).filter(
                Q(category__name__icontains = c)
            ).filter(
                Q(tags__name__icontains = t)
            )
        else:
            articles = Article.objects.all().filter(
                Q(title__icontains = q) |
                Q(content__icontains = q) |
                Q(category__name__icontains = q)
            ).filter(
                Q(category__name__icontains = c)
            )
    else:
        if t != "" and t != None:
            articles = Article.objects.filter(
                Q(status='p') &
                (
                    Q(title__icontains = q) |
                    Q(content__icontains = q) |
                    Q(category__name__icontains = q)
                )
                ).filter(
                Q(category__name__icontains = c)
                ).filter(
                Q(tags__name__icontains = t)
                )
        else:
            articles = Article.objects.filter(
                Q(status='p') &
                (
                    Q(title__icontains = q) |
                    Q(content__icontains = q) |
                    Q(category__name__icontains = q)
                )
                ).filter(
                Q(category__name__icontains = c)
                )
    paginator = Paginator(articles, 20)   # 实例化分页对象
    page = request.GET.get('page')       # 从url获取页码
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)     # 如果传入不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False   # 页数小于1，不使用分页
    context = {'page_obj': page_obj, 'is_paginated': is_paginated}
    return render(request, 'posts.html', context)

def article_detail(request, pk):
    article = Article.objects.get(id=int(pk))
    # article.views += 1
    # article.save()
    article.viewed()
    # 将markdown语法渲染成html样式
    article.content = markdown.markdown(article.content,
        extensions=[
        'markdown.extensions.fenced_code',
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        'markdown.extensions.tables',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 自动生成目录
        'markdown.extensions.toc',
        ])
    context = {"article": article}
    return render(request, 'article_detail.html', context)

def article_update(request, pk):
    article = Article.objects.get(id=int(pk))
    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("posts-page")
    context = {'form': form}
    return render(request, 'write.html', context)

def article_delete(request, pk):
    article = Article.objects.get(id=int(pk))
    if request.method == "POST":
        article.delete()
        return redirect('posts-page')
    article.name = article.title
    return render(request, 'form/delete.html', {'obj': article})

def article_download(request, pk):
    article = Article.objects.get(id=int(pk))
    file_name = article.title + ".md"
    file_content = article.content.encode("utf-8")
    file_obj = tempfile.NamedTemporaryFile()
    file_obj.name = file_name
    file_obj.write(file_content)
    file_obj.seek(0)
    res = FileResponse(file_obj)
    res["Content-Type"] = "application/octet-stream"
    res["Content-Disposition"] = "attachment; filename*=utf-8'' {}".format(escape_uri_path(file_name))
    return res

# 分类

def categories(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {"categories": categories, "tags":tags}
    return render(request, 'categories.html', context)

def create_category(request):
    form = CategoryForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories-page")
    return render(request, 'form/category_form.html', context)

def update_category(request, pk):
    category = Category.objects.get(id=int(pk))
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories-page")
    context = {'form': form}
    return render(request, 'form/category_form.html', context)

def delete_category(request, pk):
    category = Category.objects.get(id=int(pk))
    if request.method == "POST":
        category.delete()
        return redirect('categories-page')
    return render(request, 'form/delete.html', {'obj':category})

# 标签

def create_tag(request):
    form = TagForm()
    context = {'form': form}
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories-page")
    return render(request, 'form/category_form.html', context)

def update_tag(request, pk):
    tag = Tag.objects.get(id=int(pk))
    form = TagForm(instance=tag)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect("categories-page")
    context = {'form': form}
    return render(request, 'form/category_form.html', context)

def delete_tag(request, pk):
    tag = Tag.objects.get(id=int(pk))
    if request.method == "POST":
        tag.delete()
        return redirect('categories-page')
    return render(request, 'form/delete.html', {'obj':tag})

def write(request):
    form = ArticleForm
    context = {'form': form}
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts-page")
    return render(request, 'write.html', context)


def picture_page(request):
    pictures = Picture.objects.all()
    paginator = Paginator(pictures, 30)   # 实例化分页对象
    page = request.GET.get('page')       # 从url获取页码
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)     # 如果传入不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False   # 页数小于1，不使用分页
    context = {'page_obj': page_obj, 'is_paginated': is_paginated}
    return render(request, 'picture.html', context)

def upload_picture(request):
    # return render(request, '/admin/blog/picture/add/')
    return redirect('/admin/blog/picture/add/')

def page_not_found(request, exception):
    return render(request, '404.html')

def internet_server_error(request):
    return render(request, '404.html')