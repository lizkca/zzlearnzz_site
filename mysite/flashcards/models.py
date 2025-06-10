from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import math

class Flashcard(models.Model):
    PROFICIENCY_LEVELS = [
        (1, '完全不认识'),
        (2, '有点印象'),
        (3, '不太熟悉'),
        (4, '比较熟悉'),
        (5, '完全掌握'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='flashcards')
    word = models.CharField(max_length=100)
    phonetic = models.CharField(max_length=100)
    definition = models.TextField()
    example_sentence = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 学习进度追踪
    last_review = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    proficiency = models.IntegerField(choices=PROFICIENCY_LEVELS, default=1)
    streak = models.IntegerField(default=0)  # 连续正确次数

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.word
    
    def calculate_next_review(self):
        """计算下次复习时间（使用简化的间隔重复算法）"""
        if self.review_count == 0:
            # 首次学习，1小时后复习
            interval = timezone.timedelta(hours=1)
        else:
            # 基础间隔随熟练度增加
            base_interval = math.pow(2, self.proficiency - 1) * self.streak
            # 转换为天数，最少1天，最多60天
            days = min(max(1, base_interval), 60)
            interval = timezone.timedelta(days=days)
        
        self.next_review = timezone.now() + interval
        return self.next_review
    
    def update_proficiency(self, is_correct):
        """更新熟练度"""
        self.review_count += 1
        self.last_review = timezone.now()
        
        if is_correct:
            self.streak += 1
            if self.proficiency < 5:
                self.proficiency += 1
        else:
            self.streak = 0
            if self.proficiency > 1:
                self.proficiency -= 1
        
        self.calculate_next_review()
        self.save()
