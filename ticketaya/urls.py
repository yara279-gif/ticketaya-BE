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
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenBlacklistView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api_auth/", include("rest_framework.urls")),
    path("account/", include("account.urls")),
    path("match/", include("match.urls")),
    # Obtain a pair of access and refresh tokens
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Use the refresh token to get a new access token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path('Post/',include('post.urls')),
    path('parties/', include("party.urls")),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
