from django.urls import path

from apps.user import views
from apps.user.views import UserList, UserDetail, SignIn, Login, Profile, autocompletemodel
from apps.post.views import PostDetail

urlpatterns = [
    path('', SignIn.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('profile/<slug:slug>/', Profile.as_view(), name='profile'),
    path('users/', UserList.as_view(), name='user_list'),
    # path('users/<slug:slug>/', UserDetail.as_view(), name='user_detail'),
    path('users/<slug:slug>/', Profile.as_view(), name='user_detail'),
    path('posts/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    # path('users/<slug:slug>/', Profile.as_view(), name='autocomplete'),
    path('users/<slug:slug>', autocompletemodel, name='autocomplete'),
]
