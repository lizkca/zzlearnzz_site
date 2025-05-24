from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Dialogue, DialoguePractice

class DialogueTests(TestCase):
    def setUp(self):
        """测试前创建用户和对话数据"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # 创建测试对话
        self.dialogue = Dialogue.objects.create(
            title='测试对话',
            content='A: 你好！\nB: 你好！很高兴见到你。\nA: also 很高兴见到你。',
            author=self.user
        )

    def test_dialogue_list_view(self):
        """测试对话列表页面"""
        response = self.client.get(reverse('dialogues:dialogue_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试对话')

    def test_dialogue_detail_view(self):
        """测试对话详情页面"""
        # 先登录用户，这样可以看到录音按钮
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(
            reverse('dialogues:dialogue_detail', args=[self.dialogue.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试对话')
        
        # 测试对话内容的每个部分是否正确显示
        self.assertContains(response, 'A: 你好！')
        self.assertContains(response, 'B: 你好！很高兴见到你。')
        self.assertContains(response, 'A: also 很高兴见到你。')
        
        # 测试录音相关的按钮
        self.assertContains(response, 'id="startRecording"')
        self.assertContains(response, '开始录音')
        self.assertContains(response, 'id="stopRecording"')
        self.assertContains(response, '停止录音')
        self.assertContains(response, 'id="playRecording"')
        self.assertContains(response, '播放录音')
        
        # 测试练习相关的元素
        self.assertContains(response, '练习次数')

    def test_dialogue_create_view(self):
        """测试创建对话功能"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': '新对话',
            'content': 'A: Hello!\nB: Hi there!',
        }
        response = self.client.post(reverse('dialogues:dialogue_create'), data)
        self.assertEqual(response.status_code, 302)  # 重定向状态码
        self.assertTrue(Dialogue.objects.filter(title='新对话').exists())

    def test_dialogue_practice_creation(self):
        """测试创建练习记录"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('dialogues:start_practice', args=[self.dialogue.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            DialoguePractice.objects.filter(
                user=self.user,
                dialogue=self.dialogue
            ).exists()
        )

    def test_unauthorized_dialogue_creation(self):
        """测试未登录用户无法创建对话"""
        data = {
            'title': '未授权对话',
            'content': 'A: Test\nB: Test',
        }
        response = self.client.post(reverse('dialogues:dialogue_create'), data)
        self.assertEqual(response.status_code, 302)  # 重定向到登录页面
        self.assertFalse(Dialogue.objects.filter(title='未授权对话').exists())

    def test_dialogue_practice_list(self):
        """测试用户的练习记录列表"""
        self.client.login(username='testuser', password='testpass123')
        # 创建一些练习记录
        DialoguePractice.objects.create(
            user=self.user,
            dialogue=self.dialogue,
            practice_count=5
        )
        response = self.client.get(reverse('dialogues:practice_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试对话')
        self.assertContains(response, '练习次数：5')
