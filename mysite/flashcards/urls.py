from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.flashcard_list, name='flashcard_list'),
    path('detail/<int:pk>/', views.flashcard_detail, name='flashcard_detail'),
    path('create/', views.flashcard_create, name='flashcard_create'),
    path('edit/<int:pk>/', views.flashcard_edit, name='flashcard_edit'),
    path('delete/<int:pk>/', views.flashcard_delete, name='flashcard_delete'),
]