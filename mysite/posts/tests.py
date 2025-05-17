from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

class PostTests(TestCase):
    def setUp(self):
        """测试前的初始化设置"""
        self.client = Client()
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        # 设置URL，添加命名空间
        self.post_list_url = reverse('posts:post_list')
        self.post_create_url = reverse('posts:post_create')

    def test_post_list_view(self):
        """测试文章列表页面"""
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')

    def test_post_create_view_without_login(self):
        """测试未登录用户创建文章"""
        response = self.client.get(self.post_create_url)
        self.assertRedirects(response, f'/users/login/?next={self.post_create_url}')

    def test_post_create_view_with_login(self):
        """测试已登录用户创建文章"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.post_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')

    def test_post_create(self):
        """测试创建新文章"""
        self.client.login(username='testuser', password='testpassword123')
        new_post_data = {
            'title_cn': '测试文章',
            'content_cn': '这是一篇测试文章的中文内容',
            'title_en': 'Test Article',
            'content_en': 'This is the English content of the test article'
        }
        response = self.client.post(self.post_create_url, new_post_data)
        self.assertTrue(Post.objects.filter(title_cn='测试文章').exists())
        new_post = Post.objects.get(title_cn='测试文章')
        self.assertRedirects(response, reverse('posts:post_detail', args=[new_post.id]))

    def test_post_language_switch(self):
        """测试文章语言切换功能"""
        self.client.login(username='testuser', password='testpassword123')
        post = Post.objects.create(
            title_cn='测试文章',
            content_cn='中文内容',
            title_en='Test Article',
            content_en='English content',
            author=self.user
        )
        response = self.client.get(reverse('posts:post_detail', args=[post.id]))
        self.assertContains(response, '测试文章')
        self.assertContains(response, 'Test Article')
        self.assertContains(response, '中文内容')
        self.assertContains(response, 'English content')

    def test_post_update(self):
        """测试更新文章"""
        self.client.login(username='testuser', password='testpassword123')
        post = Post.objects.create(
            title_cn='原标题',
            content_cn='原内容',
            title_en='Original Title',
            content_en='Original Content',
            author=self.user
        )
        update_url = reverse('posts:post_update', args=[post.id])
        updated_data = {
            'title_cn': '更新后的标题',
            'content_cn': '更新后的内容',
            'title_en': 'Updated Title',
            'content_en': 'Updated Content'
        }
        response = self.client.post(update_url, updated_data)
        post.refresh_from_db()
        self.assertEqual(post.title_cn, '更新后的标题')
        self.assertEqual(post.title_en, 'Updated Title')

    def test_post_delete(self):
        """测试删除文章"""
        self.client.login(username='testuser', password='testpassword123')
        post = Post.objects.create(
            title_cn='待删除文章',
            content_cn='待删除内容',
            title_en='Article to Delete',
            content_en='Content to Delete',
            author=self.user
        )
        delete_url = reverse('posts:post_delete', args=[post.id])
        response = self.client.post(delete_url)
        self.assertFalse(Post.objects.filter(id=post.id).exists())
        self.assertRedirects(response, reverse('posts:post_list'))

    def test_post_author_restriction(self):
        """测试非作者无法编辑/删除文章"""
        # 创建另一个用户
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        # 创建一篇文章
        post = Post.objects.create(
            title_cn='测试文章',
            content_cn='内容',
            title_en='Test Article',
            content_en='Content',
            author=self.user
        )
        self.client.login(username='otheruser', password='testpass123')
        
        # 尝试更新文章
        update_url = reverse('posts:post_update', args=[post.id])
        response = self.client.post(update_url, {
            'title_cn': '未授权的更新',
            'content_cn': '未授权的内容',
            'title_en': 'Unauthorized Update',
            'content_en': 'Unauthorized Content'
        })
        self.assertEqual(response.status_code, 403)
        
        # 尝试删除文章
        delete_url = reverse('posts:post_delete', args=[post.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Post.objects.filter(id=post.id).exists())
