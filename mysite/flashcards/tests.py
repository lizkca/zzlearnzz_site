from django.test import TestCase, Client
from django.urls import reverse
from .models import Flashcard

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
