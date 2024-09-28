from django.contrib import admin
from .models import Match

# Register your models here.


class matchadmin(admin.ModelAdmin):
    list_display = [
        "name",
        "team1",
        "team2",
        "date",
        "time",
        "stadium",
        "image",
        "no_tickets",
        "ticket_price",
        "avilable",
    ]


admin.site.register(Match, matchadmin)
