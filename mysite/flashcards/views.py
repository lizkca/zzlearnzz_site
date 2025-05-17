from django.shortcuts import render, get_object_or_404
from .models import Flashcard
from posts.models import Post

def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_date')[:5]  # 获取最新的5篇文章
    else:
        posts = None
    return render(request, 'flashcards/home.html', {
        'posts': posts,
        'is_authenticated': request.user.is_authenticated
    })

def flashcard_list(request):
    flashcards = Flashcard.objects.all()
    return render(request, 'flashcards/flashcard_list.html', {'flashcards': flashcards})

def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    return render(request, 'flashcards/flashcard_detail.html', {'flashcard': flashcard})
