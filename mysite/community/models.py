from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='study_groups')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_groups')
    is_private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate base slug from name
            base_slug = slugify(self.name)
            if not base_slug:
                # Use timestamp if name generates empty slug
                import time
                base_slug = f'group-{int(time.time())}'
            
            # Ensure slug uniqueness
            slug = base_slug
            counter = 1
            while StudyGroup.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Forum(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='forums', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_solution = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.discussion.title}'

class UserReputation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reputation')
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    helpful_count = models.IntegerField(default=0)
    solution_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}\'s reputation'

class ReportedContent(models.Model):
    CONTENT_TYPES = (
        ('discussion', 'Discussion'),
        ('comment', 'Comment'),
    )
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_content')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content_id = models.IntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Report by {self.reporter.username} - {self.content_type}'
