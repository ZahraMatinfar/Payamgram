from django.urls import path, include

from apps.post.views import CreatePost, PostList, PostDetail

urlpatterns = [
    path('create/<slug:user_slug>', CreatePost.as_view(), name='create_post'),
    path('posts/',
         include([
             path('', PostList.as_view(), name='post_list'),
             path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
         ])
         ),
]
