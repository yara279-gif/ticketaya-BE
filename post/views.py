from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer , ShowPostSerializer , UpdatePostSerializer
from .permissions import IsAuthOrReadOnly 
from .renderers import UserRenderer
from rest_framework.exceptions import PermissionDenied

# ----------------------(CreatePosts)-------------------------------------------------

class CreatePosts(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def post(self, request):
        data = request.data.copy()
        data['author_id'] = request.user.id
        data['author_name'] = request.user.username
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)

# ----------------------(ShowPosts)-------------------------------------------------

class ShowPosts(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def get(self, request):
        posts = Post.objects.all() 
        serializer = ShowPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ----------------------(PostDetail)-------------------------------------------------

class PostDetail(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk) 
        serializer = ShowPostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = self.get_object(pk)
        if post.author_id != request.user:
            raise PermissionDenied("You are not the author of this post.")
        serializer = UpdatePostSerializer(post, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors)

    def delete(self, request, pk):
        post = self.get_object(pk)  
        if post.author_id != request.user:
            raise PermissionDenied("You are not the author of this post.")
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------(DoLike)-------------------------------------------------

class DoLike(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]
    
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def post(self, request ,pk):
        post = self.get_object(pk)
        user = request.user 
        if user in post.likes.all():
             post.likes.remove(user)
        else:
            post.likes.add(user)
        serializer = ShowPostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
