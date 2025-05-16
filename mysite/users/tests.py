from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        
    def test_registration_view(self):
        """测试注册页面是否可以正常访问"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        
    def test_registration_form(self):
        """测试用户注册功能"""
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        # 检查是否创建了用户
        self.assertTrue(User.objects.filter(username='testuser').exists())
        # 检查是否自动创建了用户档案
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())
        # 检查是否重定向到登录页面
        self.assertRedirects(response, reverse('login'))

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.login_url = reverse('login')
        
    def test_login_view(self):
        """测试登录页面是否可以正常访问"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        
    def test_login_success(self):
        """测试用户登录功能"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # 检查是否登录成功并重定向到首页
        self.assertRedirects(response, '/')
        
    def test_login_failure(self):
        """测试登录失败的情况"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        # 获取已经由信号创建的profile，而不是创建新的
        self.profile = Profile.objects.get(user=self.user)
        self.profile_url = reverse('profile')
        
    def test_profile_access_without_login(self):
        """测试未登录用户访问个人资料页面"""
        response = self.client.get(self.profile_url)
        # 应该重定向到登录页面
        self.assertRedirects(response, f'/users/login/?next={self.profile_url}')
        
    def test_profile_access_with_login(self):
        """测试已登录用户访问个人资料页面"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        
    def test_profile_update(self):
        """测试更新个人资料功能"""
        self.client.login(username='testuser', password='testpassword123')
        new_data = {
            'username': 'testuser',  # Include the username field
            'email': 'newemail@example.com',
            'bio': 'New bio',
            'location': 'New location',
            'birth_date': '1990-01-01'  # Add birth_date if it's required
        }
        response = self.client.post(self.profile_url, new_data)
        # 刷新数据库中的profile实例
        self.profile.refresh_from_db()
        self.user.refresh_from_db()  # Also refresh the user instance
        # 检查是否更新成功
        self.assertEqual(self.profile.bio, 'New bio')
        self.assertEqual(self.profile.location, 'New location')
        self.assertEqual(self.user.email, 'newemail@example.com')
