# Generated by Django 5.0.6 on 2024-06-10 08:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_rename_image_picture_img"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="picture",
            options={
                "ordering": ["-created"],
                "verbose_name": "图库",
                "verbose_name_plural": "图库",
            },
        ),
    ]
