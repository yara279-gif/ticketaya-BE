from django.urls import path, include
from . import views


urlpatterns = [
    path("bookticket/<pk>/", views.book_match),
]
