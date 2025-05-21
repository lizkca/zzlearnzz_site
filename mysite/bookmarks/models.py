from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    url = models.URLField(verbose_name='链接')
    description = models.TextField(blank=True, verbose_name='描述')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='用户')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '书签'
        verbose_name_plural = '书签'

    def __str__(self):
        return self.title
