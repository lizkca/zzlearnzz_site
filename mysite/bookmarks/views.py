from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bookmark
from .forms import BookmarkForm

def bookmark_list(request):
    """显示所有公开书签"""
    bookmarks = Bookmark.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'bookmarks/bookmark_list.html', {'bookmarks': bookmarks})

@login_required
def my_bookmarks(request):
    """显示用户的所有书签"""
    bookmarks = request.user.bookmarks.all()
    return render(request, 'bookmarks/my_bookmarks.html', {'bookmarks': bookmarks})

@login_required
def bookmark_create(request):
    """创建新书签"""
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
            messages.success(request, '书签已创建！')
            return redirect('bookmarks:my_bookmarks')
    else:
        form = BookmarkForm()
    return render(request, 'bookmarks/bookmark_form.html', {'form': form})
