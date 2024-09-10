from django.urls import path,include
from .  import views


urlpatterns =[
    path ('addnewmatch/',views.addmatch,name = "all_matches"),
    path ('retrive_all_match/',views.retrieve_all_match,name = "retrive_all_match"),
    path ('retriveonematch/<pk>/',views.retrieve_one_match,name = "retrive_one_match"),
    path ('updatematch/<pk>/',views.update_match,name = "update_match"),
    path ('deletematch/<pk>/',views.deletematch,name = "delete_match"),
    path ('searchmatch/',views.search_about_match,name ='searchmatch'),
]