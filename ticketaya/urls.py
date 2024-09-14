"""
URL configuration for ticketaya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from account  import views
from django.urls import path,include
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_auth/',include('rest_framework.urls')),
    path ('account/',include('account.urls')),
    path ('register/',views.register,name =  'register'),
    path ('login/',views.login,name = "login"),
    path ('profile/',views.userprofile,name = "profile"),
    path ('changepassword/',views.change_password,name= "chpassword"),
    path ('sendrestpasswordemail/',views.reset_password_email,name =  "resetpasswordemail"),
    path ('addadmin/',views.addadmin.as_view()),
    path ('resetpassword/<uid>/<token>/',views.reset_password,name = 'resetpassword'),
    path('parties/', views.PartyListView, name='party-list'),
    path('parties/create/', views.PartyCreateView, name='party-create'),
    path('parties/<int:pk>/', views.PartyRetrieveView, name='party-retrieve'),
    path('parties/<int:pk>/update/', views.PartyUpdateView, name='party-update'),
    path('parties/<int:pk>/delete/', views.PartyDeleteView, name='party-delete'),
    path('parties/search/', views.PartySearchView, name='party-search'),
]


