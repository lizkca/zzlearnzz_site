from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Flashcard
from posts.models import Post

class FlashcardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.flashcard = Flashcard.objects.create(
            word='hello',
            phonetic='həˈləʊ',
            definition='用作问候语',
            example_sentence='Hello, how are you?'
        )

    def test_flashcard_creation(self):
        """测试单词卡片创建"""
        self.assertEqual(self.flashcard.word, 'hello')
        self.assertEqual(self.flashcard.phonetic, 'həˈləʊ')
        self.assertTrue(len(self.flashcard.definition) > 0)
        self.assertTrue(len(self.flashcard.example_sentence) > 0)

    def test_home_page_link(self):
        """测试主页包含单词卡片链接"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '单词卡片')
        self.assertContains(response, reverse('flashcard_list'))

    def test_flashcard_list_view(self):
        """测试单词卡片列表页面"""
        response = self.client.get(reverse('flashcard_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/flashcard_list.html')
        self.assertContains(response, 'hello')

    def test_flashcard_detail_view(self):
        """测试单词卡片详情页面"""
        response = self.client.get(reverse('flashcard_detail', args=[self.flashcard.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/flashcard_detail.html')
        self.assertContains(response, 'hello')
        self.assertContains(response, 'həˈləʊ')

    def test_flashcard_flip(self):
        """测试单词卡片翻转功能"""
        response = self.client.get(reverse('flashcard_detail', args=[self.flashcard.id]))
        self.assertContains(response, 'class="flashcard-front"')
        self.assertContains(response, 'class="flashcard-back"')


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

    def test_home_page_blog_list_authenticated(self):
        """测试已登录用户可以看到博客列表"""
        # 登录用户
        self.client.login(username='testuser', password='testpass123')
        
        # 访问首页
        response = self.client.get(reverse('home'))
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
        
        # 验证最新的5篇文章都显示在页面上
        for post in self.posts[-5:]:  # 检查最新的5篇文章
            self.assertContains(response, post.title_cn)
            self.assertContains(response, post.content_cn[:30])  # 检查内容预览
        
        # 验证最早的文章（第6篇）不在页面上
        self.assertNotContains(response, self.posts[0].title_cn)

    def test_home_page_blog_list_unauthenticated(self):
        """测试未登录用户看不到博客列表"""
        # 访问首页
        response = self.client.get(reverse('home'))
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200)
        
        # 验证页面不包含任何文章内容
        for post in self.posts:
            self.assertNotContains(response, post.title_cn)
            
        # 验证页面包含登录和注册按钮
        self.assertContains(response, '登录')
        self.assertContains(response, '注册')

    def test_home_page_blog_section_elements(self):
        """测试博客区域的HTML元素"""
        # 登录用户
        self.client.login(username='testuser', password='testpass123')
        
        # 访问首页
        response = self.client.get(reverse('home'))
        
        # 验证博客区域的标题存在
        self.assertContains(response, '最新博客文章')
        
        # 验证"查看所有文章"按钮存在
        self.assertContains(response, '查看所有文章')
        self.assertContains(response, reverse('posts:post_list'))


class HomePageBlogLayoutTests(TestCase):
    def setUp(self):
        """测试前创建用户和博客文章"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # 创建测试文章
        self.post = Post.objects.create(
            title_cn='测试文章标题',
            content_cn='这是测试内容，用于测试卡片式布局',
            title_en='Test Article Title',
            content_en='This is test content for card layout',
            author=self.user
        )

    def test_blog_card_layout(self):
        """测试博客卡片布局的元素"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        
        # 测试卡片容器类
        self.assertContains(response, 'class="card h-100 shadow-sm"')
        
        # 测试卡片标题样式
        self.assertContains(response, 'class="card-title text-primary')
        
        # 测试卡片内容样式
        self.assertContains(response, 'class="card-text text-muted')

    def test_blog_section_header(self):
        """测试博客区域标题部分"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        
        # 测试区域标题样式
        self.assertContains(response, 'class="section-title"')
        
        # 测试"查看所有文章"按钮
        self.assertContains(response, 'class="btn btn-outline-primary"')
        self.assertContains(response, '查看所有文章')

    def test_empty_state_display(self):
        """测试无文章时的显示状态"""
        # 删除所有文章
        Post.objects.all().delete()
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        
        # 测试提示信息
        self.assertContains(response, '暂无博客文章')
        self.assertContains(response, 'class="alert alert-info"')

    def test_unauthenticated_welcome_section(self):
        """测试未登录用户欢迎区域"""
        response = self.client.get(reverse('home'))
        
        # 测试欢迎信息
        self.assertContains(response, '欢迎来到')
        self.assertContains(response, 'class="jumbotron"')


class HomePageStatisticsTests(TestCase):
    def setUp(self):
        """测试前创建测试用户"""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )

    def test_user_count_display(self):
        """测试首页显示的用户统计数量是否正确"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '当前注册用户数：2')
        
        # 创建新用户后测试数量是否更新
        User.objects.create_user(
            username='testuser3',
            password='testpass123'
        )
        response = self.client.get(reverse('home'))
        self.assertContains(response, '当前注册用户数：3')

    def test_statistics_card_style(self):
        """测试统计卡片的样式是否正确"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<div class="card mb-4">')
        self.assertContains(response, '<h5 class="card-title">网站统计</h5>')
        self.assertContains(response, '<p class="card-text">')
