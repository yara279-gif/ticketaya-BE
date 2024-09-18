from django.urls import path
from . import views

urlpatterns = [
    path('', views.PartyListView.as_view(), name='party-list'),
    path('create', views.PartyCreateView.as_view(), name='party-create'),
    path('<int:pk>', views.PartyRetrieveView.as_view(), name='party-retrieve'),
    path('<int:pk>/update', views.PartyUpdateView.as_view(), name='party-update'),
    path('<int:pk>/delete', views.PartyDeleteView.as_view(), name='party-delete'),
    path('search', views.PartySearchView.as_view(), name='party-search'),
]