from django.contrib import admin
from .models import Party, Party_user


# Register your models here.
class Partydisplay(admin.ModelAdmin):
    list_display = [
        "name",
        "performer",
        "location",
        "datetime",
        "number_of_tickets",
        "price",
    ]


class display(admin.ModelAdmin):
    list_display = ["party", "user", "total"]


admin.site.register(Party, Partydisplay)
admin.site.register(Party_user, display)
