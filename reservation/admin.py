from django.contrib import admin
from . models import match_reservation,online_match_payment


# Register your models here.

admin.site.register(match_reservation)
admin.site.register(online_match_payment)
