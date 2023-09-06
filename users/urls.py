from django.urls import path

from users.views import (LoginView, LogoutView, RegisterView, UserUpdateView, UserConfirmationSentView,
                         UserConfirmEmailView, UserConfirmedView, UserConfirmationFailedView, reset_password,
                         UserResetDoneView, UserListView, toggle_users_activity)

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),
    path('email_confirmation_sent/', UserConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', UserConfirmedView.as_view(), name='email_confirmed'),
    path('email_confirmation_failed/', UserConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('profile/', UserUpdateView.as_view(), name='profile'),

    path('password_reset/', reset_password, name='password_reset'),
    path('password_reset/done/', UserResetDoneView.as_view(), name='password_reset_done'),
    path('list/', UserListView.as_view(), name='list'),
    path('toggle_users_activity/<int:pk>', toggle_users_activity, name='toggle_users_activity'),
]
