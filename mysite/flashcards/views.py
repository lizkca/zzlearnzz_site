from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Flashcard
from posts.models import Post
from announcements.models import Announcement
from django.utils import timezone
from bookmarks.models import Bookmark

def home(request):
    announcements = Announcement.objects.filter(
        is_active=True,
        start_date__lte=timezone.now()
    ).exclude(
        end_date__lt=timezone.now()
    )
    context = {
        'announcements': announcements,
        'total_users': User.objects.count(),  # 添加用户总数
        'public_bookmarks': Bookmark.objects.filter(is_public=True).order_by('-created_at')[:6]
    }
    return render(request, 'flashcards/home.html', context)

def flashcard_list(request):
    flashcards = Flashcard.objects.all()
    return render(request, 'flashcards/flashcard_list.html', {'flashcards': flashcards})

def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    return render(request, 'flashcards/flashcard_detail.html', {'flashcard': flashcard})
