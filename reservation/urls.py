from django.urls import path, include
from . import views


urlpatterns = [
    path("bookticket/<pk>/", views.book_match),
    path("matchpayment/<int:pk>/", views.match_payment),
    path("listreservations/", views.list_all_reservations_for_admin),
    path("listuserreservations/", views.list_all_reservations_for_user),
    path("cancelreservation/<pk>/", views.cancel_reservation),
    path("updatereservation/<pk>/", views.update_reservation),
]
