from django.contrib import admin
from .models import Party,Party_user
# Register your models here.
class Partydisplay(admin.ModelAdmin):
    list_display=[
        'name',
    'performer',
    'location',
    'datetime',
    'number_of_tickets',
    'price',
    'available'
    ]
class display(admin.ModelAdmin):
    list_display=[
    'party',
    'user',
    'total',
    'card_cvv'
    ]   

admin.site.register(Party,Partydisplay)
admin.site.register(Party_user,display)