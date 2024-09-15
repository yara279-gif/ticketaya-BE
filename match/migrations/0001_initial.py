# Generated by Django 5.1 on 2024-09-06 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("team1", models.CharField(max_length=255)),
                ("team2", models.CharField(max_length=255)),
                ("date", models.DateTimeField()),
                ("time", models.TimeField()),
                ("stadium", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
