from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import SignUpView, CustomLoginView, update_email_view

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    re_path(
        r'signup/(?P<password>[a-zA-Z0-9-]*)/$', SignUpView.as_view(), name='signup'
    ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('update-email/', update_email_view, name='update_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='profile657/password_reset_form.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='profile657/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='profile657/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='profile657/password_reset_complete.html'
    ), name='password_reset_complete'),
]
