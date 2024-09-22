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
  reset_password_email,
  change_password,
  userprofile,
  login,
  register,
  update_profile,
  sendResetPasswordPage,
)

urlpatterns =[
    path('register/',register,name =  'register'),
    path('login/',login,name = "login"),
    path("logout/", user_logout, name="logout"),
    path('profile/',userprofile,name = "profile"),
    
    # admin urls user management
    path('addadmin/',addadmin.as_view()),
    path('adduser/',adduser.as_view()),
    path('retrieveuser/<int:id>/',retrieveeuser.as_view()),
    path('searchuser/<str:username>/',searchuser.as_view()),
    path('deleteuser/<int:id>/',deleteuser.as_view()),
    path('updateuser/<int:id>/',updateuser.as_view()),
    path("deleteaccount/", delete_account, name="deleteaccount"),
    path('listusers/',listusers.as_view()),
    path("updateprofile/",update_profile,name="updateprofile"),

    # password reset urls
    path('changepassword/',change_password,name= "chpassword"),
    path('sendrestpasswordemail/',reset_password_email,name =  "resetpasswordemail"),
    path("resetpasswordPage/<uid>/<token>/", sendResetPasswordPage, name="resetpassword"),
    path("resetpassword/<uid>/<token>/", reset_password, name="resetpassword"),
    
]
