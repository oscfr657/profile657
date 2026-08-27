from django.utils import timezone
from django.db.models import Q
from .models import Key


def get_current_key(site):
    now = timezone.now()
    current_keys = Key.objects.filter(
        Q(startdate__lte=now),
        Q(enddate__gte=now) | Q(enddate__isnull=True),
        Q(site=site),
    )
    current_key = current_keys.order_by('-startdate').first()
    return current_key
