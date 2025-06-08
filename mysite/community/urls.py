from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Study Group URLs
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<slug:slug>/', views.group_detail, name='group_detail'),
    path('groups/<slug:slug>/join/', views.group_join, name='group_join'),
    path('groups/<slug:slug>/leave/', views.group_leave, name='group_leave'),
    
    # Forum URLs
    path('groups/<slug:group_slug>/forums/', views.forum_list, name='forum_list'),
    path('forums/<slug:slug>/', views.forum_detail, name='forum_detail'),
    path('groups/<slug:group_slug>/forums/create/', views.forum_create, name='forum_create'),
    
    # Discussion URLs
    path('forums/<slug:forum_slug>/discussions/create/', views.discussion_create, name='discussion_create'),
    path('discussions/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/<int:pk>/edit/', views.discussion_edit, name='discussion_edit'),
    path('discussions/<int:pk>/pin/', views.discussion_pin, name='discussion_pin'),
    path('discussions/<int:pk>/lock/', views.discussion_lock, name='discussion_lock'),
    
    # Comment URLs
    path('discussions/<int:discussion_pk>/comments/create/', views.comment_create, name='comment_create'),
    path('comments/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comments/<int:pk>/solution/', views.mark_solution, name='mark_solution'),
    
    # Reputation URLs
    path('users/<str:username>/reputation/', views.user_reputation, name='user_reputation'),
    
    # Moderation URLs
    path('report/<str:content_type>/<int:content_id>/', views.report_content, name='report_content'),
    path('moderation/queue/', views.moderation_queue, name='moderation_queue'),
    path('moderation/resolve/<int:report_id>/', views.resolve_report, name='resolve_report'),
]
