from django.urls import path
from . import views

urlpatterns = [
    path('parties', views.PartyListView.as_view(), name='party-list'),
    path('parties/create', views.PartyCreateView.as_view(), name='party-create'),
    path('parties/<int:pk>', views.PartyRetrieveView.as_view(), name='party-retrieve'),
    path('parties/<int:pk>/update', views.PartyUpdateView.as_view(), name='party-update'),
    path('parties/<int:pk>/delete', views.PartyDeleteView.as_view(), name='party-delete'),
    path('parties/search', views.PartySearchView.as_view(), name='party-search'),
]