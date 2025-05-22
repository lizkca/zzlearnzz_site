from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.flashcard_list, name='flashcard_list'),
    path('detail/<int:pk>/', views.flashcard_detail, name='flashcard_detail'),
]