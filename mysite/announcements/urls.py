from django.urls import path
from . import views

app_name = 'announcements'  # 添加这行来定义命名空间

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
]