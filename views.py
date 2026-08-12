from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect

from .utils import get_current_lock

try:
    from wagtail.models import Site as WagtailSite
except:
    pass


def get_django_site(request):
    try:
        hostname = WagtailSite.find_for_request(request).hostname
        current_site = Site.objects.filter(domain__icontains=hostname).first()
    except:
        current_site = get_current_site(request)
    return current_site


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        PROFILE657_SIGNUP_LOCKED = getattr(settings, 'PROFILE657_SIGNUP_LOCKED', True)
        if PROFILE657_SIGNUP_LOCKED:
            return redirect(f'{settings.LOGIN_URL}')
        current_site = get_django_site(request)
        current_lock = get_current_lock(current_site)
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
        current_site = get_django_site(self.request)
        current_lock = get_current_lock(current_site)
        context['is_signup_locked'] = current_lock
        return context
