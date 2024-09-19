from re import search
from django.urls import path,include
from .  import views
from .views import (
  addadmin,
  adduser,
  listusers,
  retrieveeuser,
  searchuser,
  deleteuser,
  updateuser,
  user_logout,
  delete_account,
  reset_password,
)

urlpatterns =[
    path ('register/',views.register,name =  'register'),
    path ('login/',views.login,name = "login"),
    path ('profile/',views.userprofile,name = "profile"),
    path ('changepassword/',views.change_password,name= "chpassword"),
    path ('sendrestpasswordemail/',views.reset_password_email,name =  "resetpasswordemail"),
    path('addadmin/',addadmin.as_view()),
    path('adduser/',adduser.as_view()),
    path('retrieveuser/<int:id>/',retrieveeuser.as_view()),
    path('searchuser/<str:username>/',searchuser.as_view()),
    path('deleteuser/<int:id>/',deleteuser.as_view()),
    path('updateuser/<int:id>/',updateuser.as_view()),
    path('listusers/',listusers.as_view()),
    path("resetpassword/<uid>/<token>/", reset_password, name="resetpassword"),
    path("logout/", user_logout, name="logout"),
    path("deleteaccount/", delete_account, name="deleteaccount"),
    path("updateprofile/",views.update_profile,name="updateprofile")
    
]
