from django.contrib import admin
from django.utils import timezone
from .models import Key, PasswordDelegation


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'startdate', 'enddate', 'is_active')
    list_display_links = ('id', 'startdate')
    list_filter = ('startdate', 'enddate')
    search_fields = ('password',)

    @admin.display(description='Currently active', boolean=True)
    def is_active(self, obj):
        now = timezone.now()
        has_started = obj.startdate <= now
        not_ended = (obj.enddate is None) or (obj.enddate >= now)
        return has_started and not_ended


@admin.register(PasswordDelegation)
class PasswordDelegationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_email', 'trusted_user', 'get_trusted_user_email')
    search_fields = (
        'user__username', 
        'user__email', 
        'trusted_user__username', 
        'trusted_user__email'
    )
    raw_id_fields = ('user', 'trusted_user')

    @admin.display(description="User Email")
    def get_user_email(self, obj):
        return obj.user.email

    @admin.display(description="Trusted User Email")
    def get_trusted_user_email(self, obj):
        return obj.trusted_user.email
