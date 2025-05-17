from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title_cn', 'title_en', 'author', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('title_cn', 'content_cn', 'title_en', 'content_en')
    date_hierarchy = 'created_date'
