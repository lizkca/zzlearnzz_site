from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.flashcard_detail, name='flashcard_detail'),
    path('', views.home, name='home')
]