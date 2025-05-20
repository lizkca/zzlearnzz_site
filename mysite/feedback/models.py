from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('suggestion', '建议'),
        ('bug', '问题报告'),
        ('other', '其他')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, default='suggestion', verbose_name='反馈类型')
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.CharField(
        max_length=20,
        choices=[('pending', '待处理'), ('processing', '处理中'), ('resolved', '已解决')],
        default='pending',
        verbose_name='状态'
    )
    response = models.TextField(blank=True, null=True, verbose_name='官方回复')
    response_time = models.DateTimeField(blank=True, null=True, verbose_name='回复时间')
    
    class Meta:
        verbose_name = '反馈'
        verbose_name_plural = '反馈'
        ordering = ['-created_at']  # 按创建时间倒序排序
