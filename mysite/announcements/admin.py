from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'is_active', 'created_at', 'start_date', 'end_date')
    list_filter = ('is_active', 'level')
    search_fields = ('title', 'content')
