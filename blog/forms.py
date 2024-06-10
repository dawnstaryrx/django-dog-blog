from django.forms import ModelForm, TextInput, Textarea
from .models import Category, Tag, Article, Picture

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        # fields = ['name', ...]

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"

class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = "__all__"

class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = [ 'category', 'title', 'content', 'tags', 'status']
        widgets = {
            'title': TextInput(attrs={'class':'form-control', 'style': 'width: 100%; background-color: rgb(236, 239, 244);border-color: rgb(236, 239, 244); outline-color: rgba(236, 239, 244, 0.61);'}),
            'content': Textarea(attrs={'class':'form-control', 'style': 'font-size: 18px; width: 100%; height: 500px; background-color: rgb(236, 239, 244); outline-color: rgba(236, 239, 244, 0.61);'}),
        }