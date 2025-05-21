from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bookmark

class BookmarkTests(TestCase):
    def setUp(self):
        """测试前创建用户和书签"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        
        # 创建一些测试书签
        self.private_bookmark = Bookmark.objects.create(
            title='私密书签',
            url='https://example.com/private',
            description='这是一个私密书签',
            user=self.user,
            is_public=False
        )
        
        self.public_bookmark = Bookmark.objects.create(
            title='公开书签',
            url='https://example.com/public',
            description='这是一个公开书签',
            user=self.user,
            is_public=True
        )

    def test_bookmark_creation(self):
        """测试书签创建"""
        self.assertEqual(self.private_bookmark.title, '私密书签')
        self.assertEqual(self.private_bookmark.url, 'https://example.com/private')
        self.assertFalse(self.private_bookmark.is_public)
        self.assertEqual(self.private_bookmark.user, self.user)

    def test_home_page_bookmark_link(self):
        """测试导航栏包含共享书签链接"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '共享书签')
        self.assertContains(response, reverse('bookmarks:bookmark_list'))

    def test_public_bookmark_list(self):
        """测试共享书签列表页面"""
        response = self.client.get(reverse('bookmarks:bookmark_list'))
        
        # 验证公开书签显示在列表中
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '公开书签')
        self.assertContains(response, 'https://example.com/public')
        
        # 验证私密书签不显示在列表中
        self.assertNotContains(response, '私密书签')
        self.assertNotContains(response, 'https://example.com/private')

    def test_my_bookmarks_authenticated(self):
        """测试已登录用户查看自己的书签"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bookmarks:my_bookmarks'))
        
        # 验证可以看到所有自己的书签
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '私密书签')
        self.assertContains(response, '公开书签')

    def test_my_bookmarks_unauthenticated(self):
        """测试未登录用户访问我的书签"""
        response = self.client.get(reverse('bookmarks:my_bookmarks'))
        
        # 验证重定向到登录页面
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("bookmarks:my_bookmarks")}')

    def test_bookmark_create_authenticated(self):
        """测试已登录用户创建书签"""
        self.client.login(username='testuser', password='testpass123')
        
        # 创建新书签
        response = self.client.post(reverse('bookmarks:bookmark_create'), {
            'title': '新书签',
            'url': 'https://example.com/new',
            'description': '这是一个新书签',
            'is_public': True
        })
        
        # 验证创建成功并重定向
        self.assertEqual(response.status_code, 302)
        
        # 验书签已创建
        new_bookmark = Bookmark.objects.get(title='新书签')
        self.assertEqual(new_bookmark.url, 'https://example.com/new')
        self.assertTrue(new_bookmark.is_public)
        self.assertEqual(new_bookmark.user, self.user)

    def test_bookmark_create_unauthenticated(self):
        """测试未登录用户创建书签"""
        response = self.client.post(reverse('bookmarks:bookmark_create'), {
            'title': '新书签',
            'url': 'https://example.com/new',
            'description': '这是一个新书签',
            'is_public': True
        })
        
        # 验证重定向到登录页面
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("bookmarks:bookmark_create")}')

    def test_bookmark_privacy(self):
        """测试书签隐私设置"""
        # 登录其他用户
        self.client.login(username='otheruser', password='testpass123')
        
        # 访问共享书签列表
        response = self.client.get(reverse('bookmarks:bookmark_list'))
        
        # 验证可以看到其他用户的公开书签
        self.assertContains(response, '公开书签')
        
        # 验证看不到其他用户的私密书签
        self.assertNotContains(response, '私密书签')
