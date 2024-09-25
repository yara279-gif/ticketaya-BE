from django.urls import path, include
from . import views


urlpatterns = [
    path("bookticket/<pk>/", views.book_match),
    path("matchpayment/<int:pk>/", views.match_payment),
]
