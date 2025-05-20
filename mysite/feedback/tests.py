from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Feedback

class FeedbackTests(TestCase):
    def setUp(self):
        """测试前创建用户和反馈"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        
        # 创建一些测试反馈
        self.feedback1 = Feedback.objects.create(
            user=self.user,
            type='suggestion',
            title='建议1',
            content='这是第一条建议',
            status='pending'
        )
        
        self.feedback2 = Feedback.objects.create(
            user=self.user,
            type='bug',
            title='问题报告',
            content='发现了一个bug',
            status='processing'
        )
        
        self.feedback3 = Feedback.objects.create(
            user=self.user,
            type='other',
            title='已解决的反馈',
            content='这是一条已解决的反馈',
            status='resolved',
            response='感谢反馈，已解决',
            response_time=timezone.now()
        )

    def test_public_feedback_list(self):
        """测试反馈列表对所有人可见"""
        # 未登录用户也能访问
        response = self.client.get(reverse('feedback:feedback_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '建议1')
        self.assertContains(response, '问题报告')
        
        # 验证反馈按时间倒序排序
        feedbacks = response.context['feedbacks']
        self.assertEqual(list(feedbacks), [self.feedback3, self.feedback2, self.feedback1])

    def test_feedback_status_display(self):
        """测试反馈状态显示"""
        response = self.client.get(reverse('feedback:feedback_list'))
        
        # 测试待处理状态
        self.assertContains(response, 'badge-warning')
        self.assertContains(response, '待处理')
        
        # 测试处理中状态
        self.assertContains(response, 'badge-info')
        self.assertContains(response, '处理中')
        
        # 测试已解决状态
        self.assertContains(response, 'badge-success')
        self.assertContains(response, '已解决')

    def test_feedback_response_display(self):
        """测试反馈回复显示"""
        response = self.client.get(reverse('feedback:feedback_list'))
        
        # 验证有回复的反馈显示回复内容
        self.assertContains(response, '感谢反馈，已解决')
        self.assertContains(response, '官方回复')
        
        # 验证未回复的反馈不显示回复部分
        self.assertContains(response, self.feedback1.title)  # 确认未回复的反馈存在
        self.assertNotContains(response, f'<div class="mt-3 p-3 bg-light rounded"><strong>官方回复 ({self.feedback1.created_at})</strong>')

    def test_create_feedback_authentication(self):
        """测试创建反馈的权限控制"""
        # 未登录用户不能看到创建按钮
        response = self.client.get(reverse('feedback:feedback_list'))
        self.assertNotContains(response, '提交新反馈')
        
        # 登录用户可以看到创建按钮
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('feedback:feedback_list'))
        self.assertContains(response, '提交新反馈')

    def test_feedback_ordering(self):
        """测试反馈排序"""
        response = self.client.get(reverse('feedback:feedback_list'))
        feedbacks = response.context['feedbacks']
        
        # 验证按创建时间倒序排序
        self.assertTrue(
            all(a.created_at >= b.created_at 
                for a, b in zip(feedbacks, feedbacks[1:]))
        )
