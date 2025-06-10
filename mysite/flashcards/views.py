from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Flashcard
from .forms import FlashcardForm
from django.urls import reverse

@login_required
def flashcard_list(request):
    flashcards_list = Flashcard.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(flashcards_list, 12)  # 每页显示12个单词卡片
    
    page = request.GET.get('page')
    flashcards = paginator.get_page(page)
    
    return render(request, 'flashcards/flashcard_list.html', {
        'flashcards': flashcards,
        'total_count': flashcards_list.count()
    })

@login_required
def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    # 获取上一个和下一个卡片
    next_card = Flashcard.objects.filter(user=request.user, created_at__gt=flashcard.created_at).order_by('created_at').first()
    prev_card = Flashcard.objects.filter(user=request.user, created_at__lt=flashcard.created_at).order_by('-created_at').first()
    
    return render(request, 'flashcards/flashcard_detail.html', {
        'flashcard': flashcard,
        'next_card': next_card,
        'prev_card': prev_card
    })

@login_required
def flashcard_create(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = request.user
            flashcard.save()
            messages.success(request, '单词卡片创建成功！')
            return redirect('flashcard_detail', pk=flashcard.pk)
    else:
        form = FlashcardForm()
    
    return render(request, 'flashcards/flashcard_form.html', {
        'form': form,
        'title': '创建单词卡片',
        'submit_text': '创建'
    })

@login_required
def flashcard_edit(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            flashcard = form.save()
            messages.success(request, '单词卡片更新成功！')
            return redirect('flashcard_detail', pk=flashcard.pk)
    else:
        form = FlashcardForm(instance=flashcard)
    
    return render(request, 'flashcards/flashcard_form.html', {
        'form': form,
        'title': '编辑单词卡片',
        'submit_text': '更新'
    })

@login_required
def flashcard_delete(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    if request.method == 'POST':
        flashcard.delete()
        messages.success(request, '单词卡片已删除！')
        return redirect('flashcard_list')
    return render(request, 'flashcards/flashcard_confirm_delete.html', {
        'flashcard': flashcard
    })
