from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EmailUpdateForm
from .utils import get_current_key

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
    template_name = 'profile657/signup.html'

    def get(self, request, *args, **kwargs):
        PROFILE657_SIGNUP_LOCKED = getattr(settings, 'PROFILE657_SIGNUP_LOCKED', True)
        if PROFILE657_SIGNUP_LOCKED:
            current_site = get_django_site(request)
            current_key = get_current_key(current_site)
            if current_key:
                if current_key.password:
                    password = self.kwargs.get('password', None)
                    if password and password == current_key.password:
                        return super().get(request, *args, **kwargs)
                    else:
                        return redirect(f'{settings.LOGIN_URL}')
                else:
                    return super().get(request, *args, **kwargs)
            else:
                return redirect(f'{settings.LOGIN_URL}')
        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'profile657/login.html'

    def get_context_data(self, **kwargs):
        PROFILE657_SIGNUP_LOCKED = getattr(settings, 'PROFILE657_SIGNUP_LOCKED', True)
        context = super().get_context_data(**kwargs)
        is_signup_locked = True
        if PROFILE657_SIGNUP_LOCKED:
            current_site = get_django_site(self.request)
            current_key = get_current_key(current_site)
            if current_key:
                if current_key.password:
                    is_signup_locked = True
                else:
                    is_signup_locked = False
            else:
                is_signup_locked = True
            context['is_signup_locked'] = is_signup_locked
        else:
            is_signup_locked = False
        context['is_signup_locked'] = is_signup_locked
        return context


@login_required
def update_email_view(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your e-mail have been updated!")
            return redirect('update_email')
    else:
        form = EmailUpdateForm(instance=request.user)

    return render(request, 'profile657/update_email.html', {'form': form})
