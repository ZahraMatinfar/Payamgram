from django.urls import path

from apps.user.views import SignIn, Login, Profile, UserDetail, UserList

urlpatterns = [
    path('', SignIn.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('profile/<slug:slug>/', Profile.as_view(), name='profile'),
    path('user_detail/<slug:slug>/', UserDetail.as_view(), name='user_detail'),
    path('users/', UserList.as_view(), name='user_list'),
    # path('profile/',view,name='profile'),
]
