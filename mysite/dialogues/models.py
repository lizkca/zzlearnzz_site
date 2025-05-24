from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Dialogue(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='对话内容')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = '对话'
        verbose_name_plural = '对话'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dialogues:dialogue_detail', kwargs={'pk': self.pk})

class DialoguePractice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, verbose_name='对话')
    practice_count = models.IntegerField(default=0, verbose_name='练习次数')
    last_practice = models.DateTimeField(auto_now=True, verbose_name='最后练习时间')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        ordering = ['-last_practice']
        verbose_name = '练习记录'
        verbose_name_plural = '练习记录'
        unique_together = ['user', 'dialogue']  # 每个用户对每个对话只能有一条练习记录

    def __str__(self):
        return f'{self.user.username} - {self.dialogue.title}'
