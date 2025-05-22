from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Flashcard
from posts.models import Post
from announcements.models import Announcement
from django.utils import timezone
from bookmarks.models import Bookmark

def flashcard_list(request):
    flashcards_list = Flashcard.objects.all().order_by('-created_at')
    paginator = Paginator(flashcards_list, 12)  # 每页显示12个单词卡片
    
    page = request.GET.get('page')
    flashcards = paginator.get_page(page)
    
    return render(request, 'flashcards/flashcard_list.html', {
        'flashcards': flashcards,
        'total_count': flashcards_list.count()
    })

def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    # 获取上一个和下一个卡片
    next_card = Flashcard.objects.filter(created_at__gt=flashcard.created_at).order_by('created_at').first()
    prev_card = Flashcard.objects.filter(created_at__lt=flashcard.created_at).order_by('-created_at').first()
    
    return render(request, 'flashcards/flashcard_detail.html', {
        'flashcard': flashcard,
        'next_card': next_card,
        'prev_card': prev_card
    })
