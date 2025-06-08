from django.contrib import admin
from .models import StudyGroup, Forum, Discussion, Comment, UserReputation, ReportedContent

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'created_at', 'is_private')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'study_group', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum', 'author', 'created_at', 'is_pinned', 'is_locked')
    list_filter = ('is_pinned', 'is_locked', 'created_at')
    search_fields = ('title', 'content', 'author__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author', 'created_at', 'is_solution')
    list_filter = ('is_solution', 'created_at')
    search_fields = ('content', 'author__username')

@admin.register(UserReputation)
class UserReputationAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'level', 'helpful_count', 'solution_count')
    search_fields = ('user__username',)

@admin.register(ReportedContent)
class ReportedContentAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'content_type', 'created_at', 'is_resolved')
    list_filter = ('content_type', 'is_resolved', 'created_at')
    search_fields = ('reporter__username', 'reason')
