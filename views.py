from django.conf import settings
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from django.contrib import messages

from .models import PasswordDelegation
from .forms import EmailUpdateForm, CustomUserCreationForm
from .utils import get_current_key

try:
    from wagtail.models import Site as WagtailSite
except:
    pass


User = get_user_model()


def get_django_site(request):
    try:
        hostname = WagtailSite.find_for_request(request).hostname
        current_site = Site.objects.filter(domain__icontains=hostname).first()
    except:
        current_site = get_current_site(request)
    return current_site


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'profile657/signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(f'profile657:profile')
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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(f'profile657:profile')
        return super().get(request, *args, **kwargs)


@login_required
def profile_view(request):
    delegation_on = getattr(settings, 'PROFILE657_PASSWORD_DELEGATION', False)
    return render(request, 'profile657/profile.html', {delegation_on: delegation_on})


@login_required
def update_email_view(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your e-mail have been updated!")
            return redirect('profile657:update_email')
    else:
        form = EmailUpdateForm(instance=request.user)
    return render(request, 'profile657/update_email.html', {'form': form})


@login_required
def managed_users_view(request):
    if not getattr(settings, 'PROFILE657_PASSWORD_DELEGATION', False):
        raise Http404("This feature is disabled.")

    delegations = PasswordDelegation.objects.filter(trusted_user=request.user)
    return render(
        request, 'profile657/managed_users.html', {'delegations': delegations}
    )


@login_required
def reset_delegated_password_view(request, user_id):
    if not getattr(settings, 'PROFILE657_PASSWORD_DELEGATION', False):
        raise Http404("This feature is disabled.")

    delegation = get_object_or_404(
        PasswordDelegation, user_id=user_id, trusted_user=request.user
    )
    target_user = delegation.user

    if request.method == 'POST':
        form = SetPasswordForm(target_user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Password for {target_user.username} has been updated."
            )
            return redirect('profile657:managed_users')
    else:
        form = SetPasswordForm(target_user)

    return render(
        request,
        'profile657/reset_delegated_password.html',
        {'form': form, 'target_user': target_user},
    )
