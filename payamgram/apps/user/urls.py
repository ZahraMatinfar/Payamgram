from django.urls import path,re_path
from apps.user.views import UserList,UserDetail
from apps.user import views
from apps.post.views import PostDetail

urlpatterns = [
    re_path(r'^register/$', views.register, name='register'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<slug:slug>/', UserDetail.as_view(), name='user_detail'),
    path('posts/<slug:slug>/', PostDetail.as_view(),name = 'post_detail')
    ]
