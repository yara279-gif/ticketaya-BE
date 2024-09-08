from django.db import models
from account.models import User

class Post (models.Model):
    title = models.CharField(max_length=35)
    content = models.TextField ()
    author_id = models.ForeignKey(User, related_name= "Posts", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True)  
    image = models.ImageField(null=True, blank=True , default=0 )
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True , default=False)

    def __str__(self):
        return self.title


