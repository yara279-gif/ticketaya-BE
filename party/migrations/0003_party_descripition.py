# Generated by Django 5.1.1 on 2024-09-24 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0002_party_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='descripition',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
