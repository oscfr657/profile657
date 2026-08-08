from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect

from .utils import get_current_lock


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        PROFILE657_SIGNUP_LOCKED = getattr(settings, 'PROFILE657_SIGNUP_LOCKED', True)
        if PROFILE657_SIGNUP_LOCKED:
            return redirect(f'{settings.LOGIN_URL}')
        current_lock = get_current_lock()
        if current_lock:
            if current_lock.password:
                password = self.kwargs.get('password', None)
                if password and password == current_lock.password:
                    return super().get(request, *args, **kwargs)
            return redirect(f'{settings.LOGIN_URL}')
        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if settings.PROFILE657_SIGNUP_LOCKED:
            context['is_signup_locked'] = True
            return context
        current_lock = get_current_lock()
        context['is_signup_locked'] = (current_lock or current_lock.password)
        return context
