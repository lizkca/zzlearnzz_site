from django.urls import path
from . import views

app_name = 'dialogues'

urlpatterns = [
    path('', views.DialogueListView.as_view(), name='dialogue_list'),
    path('<int:pk>/', views.DialogueDetailView.as_view(), name='dialogue_detail'),
    path('create/', views.DialogueCreateView.as_view(), name='dialogue_create'),
    path('practice/<int:pk>/', views.start_practice, name='start_practice'),
    path('practice/list/', views.PracticeListView.as_view(), name='practice_list'),
]