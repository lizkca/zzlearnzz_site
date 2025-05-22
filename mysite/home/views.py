from django.shortcuts import render
from django.contrib.auth.models import User
from posts.models import Post

def home(request):
    context = {
        'total_users': User.objects.count()
    }
    
    if request.user.is_authenticated:
        context['posts'] = Post.objects.all().order_by('-created_date')[:5]
        
    return render(request, 'home/home.html', context)
