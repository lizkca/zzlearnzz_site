from django.contrib import admin
from .models import Dialogue, DialoguePractice

@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_date']
    list_filter = ['created_date', 'author']
    search_fields = ['title', 'content']

@admin.register(DialoguePractice)
class DialoguePracticeAdmin(admin.ModelAdmin):
    list_display = ['user', 'dialogue', 'practice_count', 'last_practice']
    list_filter = ['user', 'last_practice']
    search_fields = ['user__username', 'dialogue__title']
