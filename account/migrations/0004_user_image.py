# Generated by Django 4.2.13 on 2024-09-14 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_delete_match"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(
                default="images/24/9/12/profile.png", upload_to="images/%y/%m/%d"
            ),
        ),
    ]
