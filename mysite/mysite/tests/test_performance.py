from django.test import TestCase, Client
from django.urls import reverse
import time

class PerformanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_home_page_load_time(self):
        start_time = time.time()
        response = self.client.get(reverse('home:home'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        load_time = end_time - start_time
        print(f'Home page load time: {load_time:.2f} seconds')
        # 设置合理的加载时间阈值
        self.assertLess(load_time, 1.0)  # 期望加载时间小于1秒
        
    def test_community_list_load_time(self):
        start_time = time.time()
        response = self.client.get(reverse('community:group_list'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        load_time = end_time - start_time
        print(f'Community list load time: {load_time:.2f} seconds')
        self.assertLess(load_time, 1.0)
