from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Announcement

class AnnouncementTests(TestCase):
    def setUp(self):
        """测试前的初始化设置"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.announcement = Announcement.objects.create(
            title='测试公告',
            content='这是一条测试公告',
            is_active=True,
            level='info',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7)
        )

    def test_announcement_creation(self):
        """测试创建公告"""
        self.assertEqual(self.announcement.title, '测试公告')
        self.assertEqual(self.announcement.content, '这是一条测试公告')
        self.assertTrue(self.announcement.is_active)
        self.assertEqual(self.announcement.level, 'info')

    def test_announcement_validity(self):
        """测试公告有效性"""
        # 测试有效公告
        self.assertTrue(self.announcement.is_valid())
        
        # 测试未激活公告
        self.announcement.is_active = False
        self.announcement.save()
        self.assertFalse(self.announcement.is_valid())
        
        # 测试过期公告
        self.announcement.is_active = True
        self.announcement.end_date = timezone.now() - timedelta(days=1)
        self.announcement.save()
        self.assertFalse(self.announcement.is_valid())
        
        # 测试未开始公告
        self.announcement.start_date = timezone.now() + timedelta(days=1)
        self.announcement.end_date = timezone.now() + timedelta(days=7)
        self.announcement.save()
        self.assertFalse(self.announcement.is_valid())

    def test_announcement_list_display(self):
        """测试公告在公告列表页显示"""
        response = self.client.get(reverse('announcements:announcement_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试公告')
        self.assertContains(response, '这是一条测试公告')

    def test_announcement_admin_access(self):
        """测试管理员访问公告管理界面"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/announcements/announcement/')
        self.assertEqual(response.status_code, 200)

    def test_announcement_level_display(self):
        """测试不同级别公告的显示"""
        levels = ['info', 'warning', 'danger']
        for level in levels:
            announcement = Announcement.objects.create(
                title=f'{level}级别公告',
                content=f'这是一条{level}级别的公告',
                level=level,
                is_active=True,
                start_date=timezone.now()
            )
            response = self.client.get(reverse('announcements:announcement_list'))
            self.assertContains(response, f'{level}级别公告')
            self.assertContains(response, f'alert-{level}')

    def test_expired_announcement_not_shown(self):
        """测试过期公告不显示"""
        expired_announcement = Announcement.objects.create(
            title='过期公告',
            content='这是一条过期公告',
            is_active=True,
            start_date=timezone.now() - timedelta(days=14),
            end_date=timezone.now() - timedelta(days=7)
        )
        response = self.client.get(reverse('announcements:announcement_list'))
        self.assertNotContains(response, '过期公告')

    def test_future_announcement_not_shown(self):
        """测试未来公告不显示"""
        future_announcement = Announcement.objects.create(
            title='未来公告',
            content='这是一条未来公告',
            is_active=True,
            start_date=timezone.now() + timedelta(days=7)
        )
        response = self.client.get(reverse('announcements:announcement_list'))
        self.assertNotContains(response, '未来公告')
