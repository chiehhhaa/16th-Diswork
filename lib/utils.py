from datetime import datetime
from django.utils import timezone

def to_aware_datetime(time):
    naive_datetime = datetime.strptime(time, "%Y-%m-%dT%H:%M")
    aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
    return aware_datetime