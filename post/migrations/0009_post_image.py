# Generated by Django 5.1.1 on 2024-09-23 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0008_remove_post_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(default=0, upload_to=""),
        ),
    ]
