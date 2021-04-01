from django.urls import path, include

from apps.post.views import CreatePost, PostList, PostDetail, DeleteComment, EditPost, DeletePost, LikePost

urlpatterns = [
    path('create/', CreatePost.as_view(), name='create_post'),
    path('posts/',
         include([
             path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
             path('edit/<slug:slug>', EditPost.as_view(), name='edit_post'),
             path('delete/<slug:slug>', DeletePost.as_view(), name='delete_post'),
             path('like/<slug:slug>', LikePost.as_view(), name='like_post'),
         ])
         ),
    path('comment/delete/<int:pk>', DeleteComment.as_view(), name='delete_comment'),

]
