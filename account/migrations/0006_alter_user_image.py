# Generated by Django 3.2.25 on 2024-09-09 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_alter_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(
                default="download.jpg", upload_to="images/%y/%m/%d"
            ),
        ),
    ]
