from rest_framework import serializers
from . models import Post
from .utils import Util

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'author_id','author_name','created_at','image']
        
class ShowPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content','author_name','created_at','image','likes']
        
class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content','author_name','image']
        
        