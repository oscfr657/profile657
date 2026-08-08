from django.contrib import admin
from django.utils import timezone
from .models import Lock


@admin.register(Lock)
class LockAdmin(admin.ModelAdmin):
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
