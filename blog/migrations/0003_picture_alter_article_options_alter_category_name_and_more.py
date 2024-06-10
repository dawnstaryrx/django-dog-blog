# Generated by Django 5.0.6 on 2024-06-10 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_tag_article_views_article_tags"),
    ]

    operations = [
        migrations.CreateModel(
            name="Picture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="名称")),
                ("image", models.ImageField(upload_to="image", verbose_name="图片")),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
            ],
            options={
                "verbose_name": "图片",
                "verbose_name_plural": "图片",
                "ordering": ["-created"],
            },
        ),
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ["-published"],
                "verbose_name": "文章",
                "verbose_name_plural": "文章",
            },
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=50, verbose_name="分类名称"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=20, verbose_name="名称"),
        ),
    ]
