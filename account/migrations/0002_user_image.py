# Generated by Django 3.2.25 on 2024-09-09 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(
                default="static\x07dmin\\img\\download.png", upload_to="images/%y/%m/%d"
            ),
        ),
    ]
