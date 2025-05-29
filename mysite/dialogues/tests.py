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
        
        # 测试朗读相关的按钮和控件
        self.assertContains(response, 'id="readDialogue"')
        self.assertContains(response, '朗读对话')
        self.assertContains(response, 'id="stopReading"')
        self.assertContains(response, '停止朗读')
        self.assertContains(response, 'class="read-controls"')
        
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
        self.assertEqual(DialoguePractice.objects.count(), 1)

    def test_dialogue_practice_list(self):
        """测试用户的练习记录列表"""
        self.client.login(username='testuser', password='testpass123')
        # 显式创建测试数据
        practice, created = DialoguePractice.objects.get_or_create(
            user=self.user,  # 注意这里使用self.user而不是self.testuser
            dialogue=self.dialogue,
            defaults={'practice_count': 5}
        )
        if not created:
            practice.practice_count = 5
            practice.save()
            
        response = self.client.get(reverse('dialogues:practice_list'))
        self.assertContains(response, '练习次数：5')

class DialogueUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 创建作者用户
        cls.author = User.objects.create_user(username='authoruser', password='12345')
        # 创建其他用户
        cls.other_user = User.objects.create_user(username='otheruser', password='12345')
        # 创建测试对话
        cls.dialogue = Dialogue.objects.create(
            title='测试对话',
            content='测试内容',
            author=cls.author
        )

    def test_other_user_cant_edit(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('dialogues:dialogue_edit', args=[self.dialogue.pk]))
        self.assertEqual(response.status_code, 403)

    def test_edit_updates_object(self):
        self.client.login(username='authoruser', password='12345')  # 使用类方法创建的作者用户
        response = self.client.post(
            reverse('dialogues:dialogue_edit', args=[self.dialogue.pk]),
            {'title': 'Updated', 'content': 'Updated Content'}
        )
        self.assertRedirects(response, reverse('dialogues:dialogue_list'))
        self.dialogue.refresh_from_db()
        self.assertEqual(self.dialogue.title, 'Updated')
