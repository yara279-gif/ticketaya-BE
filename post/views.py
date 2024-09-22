from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Post_comment
from .serializers import (
    PostSerializer,
    ShowPostSerializer,
    UpdatePostSerializer,
    CommentSerializer,
)
from .permissions import IsAuthOrReadOnly
from .renderers import UserRenderer
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

# ----------------------(CreatePosts)-------------------------------------------------


class CreatePosts(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def post(self, request):
        data = request.data.copy()
        data["author_id"] = request.user.id
        data["author_name"] = request.user.username
        data["author_image"] = request.user.image
        serializer = PostSerializer(data=data, context={"request": request})
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
        serializer = ShowPostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------(ListMyPosts)-------------------------------------------------


class ListMyPosts(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def get(self, request):
        posts = Post.objects.filter(author_id=request.user.id)
        serializer = ShowPostSerializer(posts, many=True, context={"request": request})
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
        serializer = ShowPostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = self.get_object(pk)
        if post.author_id != request.user:
            raise PermissionDenied("You are not the author of this post.")
        serializer = UpdatePostSerializer(
            post, data=request.data, partial=True, context={"request": request}
        )
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

    def post(self, request, pk):
        post = self.get_object(pk)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        serializer = ShowPostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------(CreateComments)-------------------------------------------------


class CreateComment(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def post(self, request, post_pk):
        data = request.data.copy()
        data["author_id"] = request.user.id
        data["author_name"] = request.user.username
        try:
            post = Post.objects.get(pk=post_pk)
            data["post_id"] = post.id
            data["post_title"] = post.title
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ValidationError(serializer.errors)


# ----------------------(CommentDetail)-------------------------------------------------


class CommentDetail(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def get_object(self, comment_pk):
        try:
            return Post_comment.objects.get(pk=comment_pk)
        except Post_comment.DoesNotExist:
            raise Http404

    def get(self, request, post_pk, comment_pk):
        try:
            post = Post.objects.get(pk=post_pk)
            comment = self.get_object(comment_pk)
            serializer = CommentSerializer(
                comment, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, post_pk, comment_pk):
        try:
            post = Post.objects.get(pk=post_pk)
            comment = self.get_object(comment_pk)
            if comment.author_id != request.user:
                raise PermissionDenied("You are not allowed to edit this comment.")

            serializer = CommentSerializer(
                comment, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise ValidationError(serializer.errors)

        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, post_pk, comment_pk):
        comment = self.get_object(comment_pk)

        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if (
            comment.author_id == request.user
            or comment.author_id == post.author_id
            or request.user.is_admin
        ):
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied("You are not allowed to delete this comment.")


# ----------------------(ListPostComments)-------------------------------------------------


class ListPostComments(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthOrReadOnly]

    def get(self, request, post_id):
        comments = Post_comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(
            comments, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------(LikeComment)-------------------------------------------------


class LikeComment(APIView):
    def get_object(self, comment_pk):
        try:
            return Post_comment.objects.get(pk=comment_pk)
        except Post_comment.DoesNotExist:
            raise Http404

    def post(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)

        serializer = CommentSerializer(comment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
