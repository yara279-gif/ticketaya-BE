from django.urls import path 
from .  import views



urlpatterns =[
    path ('create/',views.CreatePosts.as_view(), name =  'createPost'),
    path ('show/',views.ShowPosts.as_view(), name =  'showPosts'),
    path ('Update/<int:pk>',views.PostDetail.as_view(), name = 'PostDetail'),
    path ('likes/<int:pk>',views.DoLike.as_view(), name = 'likes'),
    
    

]


