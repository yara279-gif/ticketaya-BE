# Generated by Django 5.1.1 on 2024-09-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_alter_user_is_admin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
