from django.shortcuts import render, get_object_or_404
from .models import Flashcard

def home(request):
    return render(request, 'flashcards/home.html')

def flashcard_list(request):
    flashcards = Flashcard.objects.all()
    return render(request, 'flashcards/flashcard_list.html', {'flashcards': flashcards})

def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    return render(request, 'flashcards/flashcard_detail.html', {'flashcard': flashcard})
