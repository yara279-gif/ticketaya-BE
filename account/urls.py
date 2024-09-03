from re import search
from django.urls import path,include
from .  import views
from .views import addadmin,adduser, retrieveeuser, searchuser,deleteuser, updateuser

urlpatterns =[
    path ('register/',views.register,name =  'register'),
    path ('login/',views.login,name = "login"),
    path ('profile/',views.userprofile,name = "profile"),
    path ('changepassword/',views.change_password,name= "chpassword"),
    path ('sendrestpasswordemail/',views.reset_password_email,name =  "resetpasswordemail"),
    path('addadmin/',addadmin.as_view()),
    path('adduser/',adduser.as_view()),
    path('retrieveuser/',retrieveeuser.as_view()),
    path('searchuser/',searchuser.as_view()),
    path('deleteuser/',deleteuser.as_view()),
    path('updateuser/',updateuser.as_view()),

]