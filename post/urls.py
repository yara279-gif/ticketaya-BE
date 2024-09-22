from django.urls import path
from .views import (
    CreatePosts,
    ShowPosts,
    DoLike,
    PostDetail,
    ListMyPosts,
    CreateComment,
    CommentDetail,
    ListPostComments,
    LikeComment,
)


urlpatterns = [
    path("create/", CreatePosts.as_view(), name="createPost"),
    path("show/", ShowPosts.as_view(), name="showPosts"),
    path("myposts/", ListMyPosts.as_view(), name="listmyposts"),
    path("Update/<int:pk>", PostDetail.as_view(), name="PostDetail"),
    path("likes/<int:pk>", DoLike.as_view(), name="likes"),
    path("comment/<int:post_pk>", CreateComment.as_view(), name="CreateComment"),
    path(
        "<int:post_pk>/commentdetail/<int:comment_pk>",
        CommentDetail.as_view(),
        name="CommentDetail",
    ),
    path(
        "listcomments/<int:post_id>",
        ListPostComments.as_view(),
        name="ListPostComments",
    ),
    path("likecomment/<int:comment_pk>", LikeComment.as_view(), name="LikeComment"),
]
