from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Flashcard
from posts.models import Post

class FlashcardTests(TestCase):
    def setUp(self):
        """测试前创建用户和单词卡片"""
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

    def test_flashcard_navigation(self):
        """测试单词卡片导航功能"""
        # 创建额外的卡片用于测试导航
        flashcard2 = Flashcard.objects.create(
            word='world',
            phonetic='wɜːld',
            definition='世界',
            example_sentence='Hello, world!'
        )
        
        response = self.client.get(reverse('flashcard_detail', args=[self.flashcard.id]))
        self.assertContains(response, '下一个')
        self.assertContains(response, reverse('flashcard_detail', args=[flashcard2.id]))

    def test_flashcard_pagination(self):
        """测试单词卡片分页功能"""
        # 创建13个卡片以触发分页（默认每页12个）
        for i in range(12):
            Flashcard.objects.create(
                word=f'word{i}',
                phonetic=f'phonetic{i}',
                definition=f'definition{i}',
                example_sentence=f'example{i}'
            )
        
        response = self.client.get(reverse('flashcard_list'))
        self.assertTrue('flashcards' in response.context)
        self.assertTrue(response.context['flashcards'].has_other_pages())
