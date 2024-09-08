from django.urls import path,include
from .  import views


urlpatterns =[
    path ('register/',views.register,name =  'register'),
    path ('login/',views.login,name = "login"),
    path ('profile/',views.userprofile,name = "profile"),
    path ('changepassword/',views.change_password,name= "chpassword"),
    path ('sendrestpasswordemail/',views.reset_password_email,name =  "resetpasswordemail"),
    path ('addadmin/',views.addadmin.as_view()),
    path ('resetpassword/<uid>/<token>/',views.reset_password,name = 'resetpassword'),
 

]