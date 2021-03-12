from django.urls import path, include

from apps.post.views import CreatePost, PostList, PostDetail, DeleteComment, EditPost

urlpatterns = [
    path('create/', CreatePost.as_view(), name='create_post'),
    path('posts/',
         include([
             path('', PostList.as_view(), name='post_list'),
             path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),

         ])
         ),
    path('comment/delete/<int:pk>', DeleteComment.as_view(), name='delete_comment'),
    path('edit/<slug:slug>', EditPost.as_view(), name='edit_post'),
]
