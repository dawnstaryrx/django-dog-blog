# Generated by Django 5.0.6 on 2024-06-10 08:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_remove_picture_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="picture",
            old_name="image",
            new_name="img",
        ),
    ]
