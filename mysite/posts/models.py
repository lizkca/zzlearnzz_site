from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    title_cn = models.CharField(max_length=200, verbose_name='中文标题')
    content_cn = models.TextField(verbose_name='中文内容')
    title_en = models.CharField(max_length=200, verbose_name='英文标题')
    content_en = models.TextField(verbose_name='英文内容')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title_cn

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.pk})
