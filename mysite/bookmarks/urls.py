from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('', views.bookmark_list, name='bookmark_list'),
    path('my/', views.my_bookmarks, name='my_bookmarks'),
    path('create/', views.bookmark_create, name='bookmark_create'),
]