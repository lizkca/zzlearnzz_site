from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post

class HomePageTests(TestCase):
    def setUp(self):
        """测试前创建用户和博客文章"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # 创建多篇测试文章
        self.posts = []
        for i in range(6):  # 创建6篇文章以测试只显示最新的5篇
            post = Post.objects.create(
                title_cn=f'测试文章{i}',
                content_cn=f'这是测试内容{i}',
                title_en=f'Test Article {i}',
                content_en=f'This is test content {i}',
                author=self.user
            )
            self.posts.append(post)

    def test_home_page_navigation(self):
        """测试首页导航栏"""
        response = self.client.get(reverse('home:home'))
        
        # 测试基本导航链接
        self.assertContains(response, '首页')
        self.assertContains(response, '公告')
        self.assertContains(response, '共享书签')
        self.assertContains(response, '单词卡片')
        
        # 测试未登录用户看不到的链接
        self.assertNotContains(response, '反馈意见')
        self.assertNotContains(response, '写博客')
        
        # 登录后测试
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home:home'))
        
        # 测试登录后可见的链接
        self.assertContains(response, '反馈意见')
        self.assertContains(response, '写博客')
        self.assertContains(response, '个人资料')
        self.assertContains(response, '退出')

    def test_home_page_for_anonymous(self):
        """测试未登录用户访问首页"""
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '欢迎来到我的博客')
        self.assertContains(response, '登录')
        self.assertContains(response, '注册')
        
        # 验证未登录用户看不到博客列表
        for post in self.posts:
            self.assertNotContains(response, post.title_cn)

    def test_home_page_for_authenticated(self):
        """测试已登录用户访问首页"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'欢迎回来，{self.user.username}')
        self.assertContains(response, '浏览文章')
        self.assertContains(response, '单词卡片')

    def test_home_page_blog_list(self):
        """测试首页博客列表"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home:home'))
        
        # 验证最新的5篇文章都显示在页面上
        for post in self.posts[-5:]:  # 检查最新的5篇文章
            self.assertContains(response, post.title_cn)
            self.assertContains(response, post.content_cn[:30])  # 检查内容预览
        
        # 验证最早的文章（第6篇）不在页面上
        self.assertNotContains(response, self.posts[0].title_cn)

    def test_home_page_statistics(self):
        """测试首页统计信息"""
        # 创建额外的测试用户
        User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '网站统计')
        self.assertContains(response, '当前注册用户数：2')  # 包括setUp中创建的用户
