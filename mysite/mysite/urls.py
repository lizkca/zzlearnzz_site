from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('announcements/', include('announcements.urls')),
    path('bookmarks/', include('bookmarks.urls')),  # 添加 bookmarks 的 URLs
    path('users/', include('users.urls')),  # 添加 users 的 URLs
    path('feedback/', include('feedback.urls')),  # 添加 feedback 的 URLs
    path('posts/', include('posts.urls')),  # 添加 posts 的 URLs
    path('flashcards/', include('flashcards.urls')),  # 添加 flashcards 的 URLs
    path('dialogues/', include('dialogues.urls', namespace='dialogues')),
]
