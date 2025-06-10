from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Flashcard
from .forms import FlashcardForm

class FlashcardTests(TestCase):
    def setUp(self):
        """测试前创建用户和单词卡片"""
        self.client = Client()
        
        # 创建两个用户用于测试
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        
        # 为用户1创建一个单词卡片
        self.flashcard = Flashcard.objects.create(
            user=self.user1,
            word='hello',
            phonetic='həˈləʊ',
            definition='用作问候语',
            example_sentence='Hello, how are you?'
        )

    def test_flashcard_creation(self):
        """测试单词卡片创建"""
        self.assertEqual(self.flashcard.word, 'hello')
        self.assertEqual(self.flashcard.phonetic, 'həˈləʊ')
        self.assertEqual(self.flashcard.user, self.user1)
        self.assertTrue(len(self.flashcard.definition) > 0)
        self.assertTrue(len(self.flashcard.example_sentence) > 0)

    def test_flashcard_list_view_requires_login(self):
        """测试未登录用户无法访问列表页面"""
        response = self.client.get(reverse('flashcard_list'))
        self.assertEqual(response.status_code, 302)  # 重定向到登录页面

    def test_flashcard_list_view_with_login(self):
        """测试登录用户可以访问列表页面且只能看到自己的卡片"""
        # 创建用户2的卡片
        flashcard2 = Flashcard.objects.create(
            user=self.user2,
            word='world',
            phonetic='wɜːld',
            definition='世界',
            example_sentence='Hello, world!'
        )
        
        # 用户1登录
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('flashcard_list'))
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/flashcard_list.html')
        self.assertContains(response, 'hello')  # 用户1的卡片
        self.assertNotContains(response, 'world')  # 不应该看到用户2的卡片

    def test_flashcard_detail_view_requires_login(self):
        """测试未登录用户无法访问详情页面"""
        response = self.client.get(reverse('flashcard_detail', args=[self.flashcard.id]))
        self.assertEqual(response.status_code, 302)  # 重定向到登录页面

    def test_flashcard_detail_view_with_login(self):
        """测试登录用户只能访问自己的卡片详情"""
        # 用户2登录尝试访问用户1的卡片
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(reverse('flashcard_detail', args=[self.flashcard.id]))
        self.assertEqual(response.status_code, 404)  # 应该返回404

        # 用户1登录访问自己的卡片
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('flashcard_detail', args=[self.flashcard.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hello')

    def test_create_flashcard(self):
        """测试创建单词卡片"""
        self.client.login(username='testuser1', password='testpass123')
        data = {
            'word': 'test',
            'phonetic': 'test',
            'definition': 'A test word',
            'example_sentence': 'This is a test.'
        }
        response = self.client.post(reverse('flashcard_create'), data)
        
        # 验证创建成功
        self.assertEqual(Flashcard.objects.count(), 2)
        new_flashcard = Flashcard.objects.get(word='test')
        self.assertEqual(new_flashcard.user, self.user1)

    def test_edit_flashcard(self):
        """测试编辑单词卡片"""
        # 用户2不能编辑用户1的卡片
        self.client.login(username='testuser2', password='testpass123')
        data = {
            'word': 'modified',
            'phonetic': 'modified',
            'definition': 'Modified definition',
            'example_sentence': 'Modified example'
        }
        response = self.client.post(reverse('flashcard_edit', args=[self.flashcard.id]), data)
        self.assertEqual(response.status_code, 404)
        
        # 用户1可以编辑自己的卡片
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(reverse('flashcard_edit', args=[self.flashcard.id]), data)
        self.flashcard.refresh_from_db()
        self.assertEqual(self.flashcard.word, 'modified')

    def test_delete_flashcard(self):
        """测试删除单词卡片"""
        # 用户2不能删除用户1的卡片
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(reverse('flashcard_delete', args=[self.flashcard.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Flashcard.objects.filter(id=self.flashcard.id).exists())
        
        # 用户1可以删除自己的卡片
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(reverse('flashcard_delete', args=[self.flashcard.id]))
        self.assertFalse(Flashcard.objects.filter(id=self.flashcard.id).exists())

    def test_flashcard_navigation(self):
        """测试单词卡片导航功能"""
        # 为用户1创建多个卡片用于测试导航
        flashcard2 = Flashcard.objects.create(
            user=self.user1,
            word='world',
            phonetic='wɜːld',
            definition='世界',
            example_sentence='Hello, world!'
        )
        
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('flashcard_detail', args=[self.flashcard.id]))
        self.assertContains(response, '下一个')
        self.assertContains(response, reverse('flashcard_detail', args=[flashcard2.id]))

    def test_flashcard_pagination(self):
        """测试单词卡片分页功能"""
        # 为用户1创建13个卡片以触发分页（默认每页12个）
        for i in range(12):
            Flashcard.objects.create(
                user=self.user1,
                word=f'word{i}',
                phonetic=f'phonetic{i}',
                definition=f'definition{i}',
                example_sentence=f'example{i}'
            )
        
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(reverse('flashcard_list'))
        self.assertTrue('flashcards' in response.context)
        self.assertTrue(response.context['flashcards'].has_other_pages())
