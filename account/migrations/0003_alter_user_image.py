# Generated by Django 3.2.25 on 2024-09-09 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='static/admin/img/download.png', upload_to='images/%y/%m/%d'),
        ),
    ]
