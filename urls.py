from django.urls import path, re_path

from .views import SignUpView, CustomLoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    re_path(r'signup/(?P<password>[a-zA-Z0-9-]*)/$', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
