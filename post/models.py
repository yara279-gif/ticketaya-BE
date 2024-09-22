from django.db import models
from account.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author_id = models.ForeignKey(User, related_name="Posts", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=255)
    author_image = models.ImageField(default="images/24/9/12/profile.png")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True, default=False
    )

    def __str__(self):
        return self.title


class Post_comment(models.Model):
    content = models.TextField()
    post_id = models.ForeignKey(Post, related_name="post_id", on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    author_id = models.ForeignKey(
        User, related_name="author_comment", on_delete=models.CASCADE
    )
    author_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name="commens_likes", blank=True, default=False
    )

    def __str__(self):
        return self.content
