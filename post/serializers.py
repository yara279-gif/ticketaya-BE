from rest_framework import serializers
from . models import Post ,Post_comment
from .utils import Util

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'author_id','author_name','author_image','created_at','image']
        
class ShowPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content','author_name','author_image','created_at','image','likes']
    
    # if image is not provided, set it to default image
    def validate(self, data):
        if 'image' not in self.initial_data:
            data['image'] = "0" # media/0
        return data
      
class ShowPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content','author_id' ,'author_name','created_at','image','likes']
        
class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'content','author_name','author_image','image']
        
class CommentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Post_comment
        fields = ['id','content','post_id','post_title','author_id','author_name','created_at','likes']