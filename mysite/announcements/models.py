from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    is_active = models.BooleanField('是否激活', default=True)
    level = models.CharField('重要程度', max_length=20, choices=[
        ('info', '普通'),
        ('warning', '警告'),
        ('danger', '重要')
    ], default='info')
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    start_date = models.DateTimeField('开始时间', default=timezone.now)
    end_date = models.DateTimeField('结束时间', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '网站公告'
        verbose_name_plural = '网站公告'

    def __str__(self):
        return self.title

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.end_date and now > self.end_date:
            return False
        return now >= self.start_date
