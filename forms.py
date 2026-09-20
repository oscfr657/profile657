from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import PasswordDelegation

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Required to reset your password if necessary."
    )
    trusted_manager_email = forms.EmailField(
        required=False, 
        help_text="Enter an email address of an existing user who will be allowed to reset your password."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        delegation_enabled = getattr(settings, 'PROFILE657_PASSWORD_DELEGATION', False)
        
        if not delegation_enabled:
            self.fields.pop('trusted_manager_email', None)

    def clean_trusted_manager_email(self):
        email = self.cleaned_data.get('trusted_manager_email')
        if email:
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError("No user was found with this email address.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            
            delegation_enabled = getattr(settings, 'PROFILE657_PASSWORD_DELEGATION', False)
            trusted_email = self.cleaned_data.get('trusted_manager_email')
            
            if delegation_enabled and trusted_email:
                trusted_user = User.objects.get(email=trusted_email)
                PasswordDelegation.objects.create(user=user, trusted_user=trusted_user)
                
        return user


class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {'email': 'E-mail'}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (
            email
            and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists()
        ):
            raise forms.ValidationError('The e-mailadress is wrong.')
        return email
