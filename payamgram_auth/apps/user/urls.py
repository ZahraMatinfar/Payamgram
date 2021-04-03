from django.contrib.auth import views
from django.urls import path, include, re_path

from apps.user.views import Signup, Login, Logout, ProfileView, FindUser, ConfirmRequestView, DeleteRequestView, \
    EditUserProfileView, change_password, ActivateView, \
    autocomplete, VerifySMS, PasswordResetView, EditUser

urlpatterns = [path('signing/', Signup.as_view(), name='signing'),
               path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),  # ??
               path('send_sms/<slug:slug>/', VerifySMS.as_view(), name='send_sms'),
               path('activate/<slug:slug>/', VerifySMS.as_view(), name='activate_sms'),
               path('accounts/',
                    include([
                        path('login/', Login.as_view(), name='login'),
                        path('logout', Logout.as_view(), name='logout'),
                    ])
                    ),
               path('profile/<slug:slug>/', ProfileView.as_view(), name='profile'),
               path('request/<slug:slug>/', ConfirmRequestView.as_view(), name='confirm_request'),
               path('delete/<slug:slug>/', DeleteRequestView.as_view(), name='delete_request'),
               path('users/', FindUser.as_view(), name='user_list'),
               path('edits/<slug:slug>/', EditUserProfileView.as_view(), name="edit-user-profile"),
               path('edit_profile/<slug:slug>/', EditUserProfileView.as_view(), name="edit-user-profile"),
               path('edit_account/<slug:slug>/', EditUser.as_view(), name="edit-account"),
               re_path(r'^password/$', change_password, name='change_password'),
               path('find/', FindUser.as_view(), name='find_user'),
               path('search/', autocomplete, name='search-view'),
               path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
               path('password_reset/mobile', PasswordResetView.as_view(), name='password_reset_mobile'),
               path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
               path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
               path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
               ]
