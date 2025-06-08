from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import StudyGroup, Forum, Discussion, Comment, UserReputation, ReportedContent
from django.contrib.auth import get_user_model

User = get_user_model()
# Study Group Views
@login_required
def group_list(request):
    # Only show groups with valid slugs
    groups = StudyGroup.objects.exclude(slug='').annotate(member_count=Count('members'))
    return render(request, 'community/group_list.html', {'groups': groups})

@login_required
def group_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_private = request.POST.get('is_private', False) == 'on'
        
        if not name:
            messages.error(request, '小组名称不能为空')
            return render(request, 'community/group_form.html')
            
        try:
            # Create group and save to generate slug
            group = StudyGroup.objects.create(
                name=name,
                description=description,
                admin=request.user,
                is_private=is_private
            )
            # Add current user as member
            group.members.add(request.user)
            messages.success(request, '学习小组创建成功！')
            
            # Double check we have a valid slug
            if not group.slug:
                group.save()  # Force slug generation
                
            if not group.slug:
                messages.error(request, '小组创建失败：无法生成有效的URL')
                group.delete()
                return render(request, 'community/group_form.html')
                
            return redirect('community:group_detail', slug=group.slug)
        except Exception as e:
            messages.error(request, f'创建小组时出错: {str(e)}')
            return render(request, 'community/group_form.html')
    return render(request, 'community/group_form.html')

@login_required
def group_detail(request, slug):
    group = get_object_or_404(StudyGroup, slug=slug)
    if group.is_private and request.user not in group.members.all():
        messages.error(request, 'This is a private group.')
        return redirect('community:group_list')
    return render(request, 'community/group_detail.html', {'group': group})

@login_required
def group_join(request, slug):
    group = get_object_or_404(StudyGroup, slug=slug)
    if request.user not in group.members.all():
        if group.is_private:
            messages.error(request, 'This is a private group. You need an invitation to join.')
            return redirect('community:group_list')
        group.members.add(request.user)
        messages.success(request, f'You have joined {group.name}!')
    return redirect('community:group_detail', slug=slug)

@login_required
def group_leave(request, slug):
    group = get_object_or_404(StudyGroup, slug=slug)
    if request.user in group.members.all():
        if request.user == group.admin:
            messages.error(request, 'Group admin cannot leave the group.')
            return redirect('community:group_detail', slug=slug)
        group.members.remove(request.user)
        messages.success(request, f'You have left {group.name}.')
    return redirect('community:group_list')

# Forum Views
@login_required
def forum_list(request, group_slug):
    group = get_object_or_404(StudyGroup, slug=group_slug)
    if group.is_private and request.user not in group.members.all():
        messages.error(request, 'This is a private group.')
        return redirect('community:group_list')
    forums = Forum.objects.filter(study_group=group)
    return render(request, 'community/forum_list.html', {'forums': forums, 'group': group})

@login_required
def forum_create(request, group_slug):
    group = get_object_or_404(StudyGroup, slug=group_slug)
    if request.user != group.admin and not request.user.is_staff:
        messages.error(request, 'Only group admin can create forums.')
        return redirect('community:group_detail', slug=group_slug)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        forum = Forum.objects.create(
            name=name,
            description=description,
            study_group=group
        )
        messages.success(request, 'Forum created successfully!')
        return redirect('community:forum_detail', slug=forum.slug)
    return render(request, 'community/forum_form.html', {'group': group})

@login_required
def forum_detail(request, slug):
    forum = get_object_or_404(Forum, slug=slug)
    if forum.study_group and forum.study_group.is_private and request.user not in forum.study_group.members.all():
        messages.error(request, 'This forum belongs to a private group.')
        return redirect('community:group_list')
    discussions = Discussion.objects.filter(forum=forum).order_by('-is_pinned', '-created_at')
    return render(request, 'community/forum_detail.html', {'forum': forum, 'discussions': discussions})

# Discussion Views
@login_required
def discussion_create(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)
    if forum.study_group and forum.study_group.is_private and request.user not in forum.study_group.members.all():
        messages.error(request, 'This forum belongs to a private group.')
        return redirect('community:group_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        discussion = Discussion.objects.create(
            title=title,
            content=content,
            forum=forum,
            author=request.user
        )
        messages.success(request, 'Discussion created successfully!')
        return redirect('community:discussion_detail', pk=discussion.pk)
    return render(request, 'community/discussion_form.html', {'forum': forum})

@login_required
def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if discussion.forum.study_group and discussion.forum.study_group.is_private:
        if request.user not in discussion.forum.study_group.members.all():
            messages.error(request, 'This discussion belongs to a private group.')
            return redirect('community:group_list')
    comments = Comment.objects.filter(discussion=discussion).order_by('created_at')
    return render(request, 'community/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments
    })

@login_required
def discussion_edit(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.user != discussion.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this discussion.')
        return redirect('community:discussion_detail', pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        discussion.title = title
        discussion.content = content
        discussion.save()
        messages.success(request, 'Discussion updated successfully!')
        return redirect('community:discussion_detail', pk=pk)
    return render(request, 'community/discussion_form.html', {'discussion': discussion})

@login_required
def discussion_pin(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if not request.user.is_staff and request.user != discussion.forum.study_group.admin:
        messages.error(request, 'Only staff or group admin can pin discussions.')
        return redirect('community:discussion_detail', pk=pk)
    
    discussion.is_pinned = not discussion.is_pinned
    discussion.save()
    action = 'pinned' if discussion.is_pinned else 'unpinned'
    messages.success(request, f'Discussion {action} successfully!')
    return redirect('community:discussion_detail', pk=pk)

@login_required
def discussion_lock(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if not request.user.is_staff and request.user != discussion.forum.study_group.admin:
        messages.error(request, 'Only staff or group admin can lock discussions.')
        return redirect('community:discussion_detail', pk=pk)
    
    discussion.is_locked = not discussion.is_locked
    discussion.save()
    action = 'locked' if discussion.is_locked else 'unlocked'
    messages.success(request, f'Discussion {action} successfully!')
    return redirect('community:discussion_detail', pk=pk)

# Comment Views
@login_required
def comment_create(request, discussion_pk):
    discussion = get_object_or_404(Discussion, pk=discussion_pk)
    if discussion.is_locked:
        messages.error(request, 'This discussion is locked. New comments are not allowed.')
        return redirect('community:discussion_detail', pk=discussion_pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment.objects.create(
            discussion=discussion,
            author=request.user,
            content=content
        )
        # Update user reputation for commenting
        reputation, _ = UserReputation.objects.get_or_create(user=request.user)
        reputation.points += 1
        reputation.save()
        
        messages.success(request, 'Comment added successfully!')
        return redirect('community:discussion_detail', pk=discussion_pk)
    return render(request, 'community/comment_form.html', {'discussion': discussion})

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('community:discussion_detail', pk=comment.discussion.pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        comment.content = content
        comment.save()
        messages.success(request, 'Comment updated successfully!')
        return redirect('community:discussion_detail', pk=comment.discussion.pk)
    return render(request, 'community/comment_form.html', {'comment': comment})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('community:discussion_detail', pk=comment.discussion.pk)
    
    discussion_pk = comment.discussion.pk
    if comment.is_solution:
        # Update reputation when solution is deleted
        reputation = UserReputation.objects.get(user=comment.author)
        reputation.solution_count = max(0, reputation.solution_count - 1)
        reputation.points = max(0, reputation.points - 10)
        reputation.save()
    
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('community:discussion_detail', pk=discussion_pk)

@login_required
def mark_solution(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.discussion.author and not request.user.is_staff:
        messages.error(request, 'Only the discussion author or staff can mark solutions.')
        return redirect('community:discussion_detail', pk=comment.discussion.pk)
    
    # Unmark any existing solution
    Comment.objects.filter(discussion=comment.discussion, is_solution=True).update(is_solution=False)
    
    comment.is_solution = True
    comment.save()
    
    # Update reputation
    reputation, _ = UserReputation.objects.get_or_create(user=comment.author)
    reputation.solution_count += 1
    reputation.points += 10
    reputation.save()
    
    messages.success(request, 'Comment marked as solution!')
    return redirect('community:discussion_detail', pk=comment.discussion.pk)

# Reputation Views
def user_reputation(request, username):
    user = get_object_or_404(User, username=username)
    reputation, _ = UserReputation.objects.get_or_create(user=user)
    return render(request, 'community/user_reputation.html', {'user_profile': user, 'reputation': reputation})

# Moderation Views
@login_required
def report_content(request, content_type, content_id):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        ReportedContent.objects.create(
            reporter=request.user,
            content_type=content_type,
            content_id=content_id,
            reason=reason
        )
        messages.success(request, 'Content reported successfully.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'community/report_form.html')

@login_required
def moderation_queue(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    reports = ReportedContent.objects.filter(is_resolved=False).order_by('-created_at')
    return render(request, 'community/moderation_queue.html', {'reports': reports})

@login_required
def resolve_report(request, report_id):
    if not request.user.is_staff:
        messages.error(request, 'Only staff can resolve reports.')
        return redirect('home')
    
    report = get_object_or_404(ReportedContent, pk=report_id)
    if request.method == 'POST':
        report.is_resolved = True
        report.resolution_notes = request.POST.get('resolution_notes')
        report.save()
        messages.success(request, 'Report resolved successfully!')
    return redirect('community:moderation_queue')
