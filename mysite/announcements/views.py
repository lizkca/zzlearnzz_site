from django.shortcuts import render
from django.utils import timezone
from .models import Announcement

def announcement_list(request):
    announcements = Announcement.objects.filter(
        is_active=True,
        start_date__lte=timezone.now()
    ).exclude(
        end_date__lt=timezone.now()
    )
    return render(request, 'announcements/announcement_list.html', {
        'announcements': announcements
    })
