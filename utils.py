from django.utils import timezone
from django.db.models import Q
from .models import Lock


def get_current_lock(site):
    now = timezone.now()
    current_locks = Lock.objects.filter(
        Q(startdate__lte=now),
        Q(enddate__gte=now) | Q(enddate__isnull=True),
        Q(site=site),
    )
    current_lock = current_locks.order_by('-startdate').first()
    return current_lock
