# Generated by Django 3.2.25 on 2024-09-26 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0002_party_available'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Party_user',
        ),
    ]
