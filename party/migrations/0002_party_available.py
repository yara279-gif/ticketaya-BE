# Generated by Django 3.2.25 on 2024-09-22 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
