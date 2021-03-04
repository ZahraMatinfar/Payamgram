from django.urls import path, include

from apps.user.views import Singing, Login, Logout, ProfileView, FindUser

urlpatterns = [path('signing/', Singing.as_view(), name='signing'),
               # path('accounts/', include('django.contrib.auth.urls')),
               path('accounts/',
                    include([
                        path('login/', Login.as_view(), name='login'),
                        path('logout', Logout.as_view(), name='logout'),
                    ])
                    ),
               path('profile/<slug:slug>/', ProfileView.as_view(), name='profile'),
               path('users/', FindUser.as_view(), name='user_list'),
               ]
