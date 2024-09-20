from rest_framework import serializers
from . models import Post
from .utils import Util

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'author_id','author_name','created_at','image']
    
    # if image is not provided, set it to default image
    def validate(self, data):
        if 'image' not in self.initial_data:
            data['image'] = "0"
        return data
      
class ShowPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content','author_name','created_at','image','likes']
        
class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content','author_name','image']