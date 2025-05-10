from django.urls import path
from . import views

urlpatterns = [
    path('', views.flashcard_list, name='flashcard_list'),
    path('<int:pk>/', views.flashcard_detail, name='flashcard_detail'),
]