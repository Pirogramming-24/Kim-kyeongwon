from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    # 스토리 목록: /stories/
    path('', views.story_list_view, name='list'),
    
    # 스토리 생성: /stories/create/
    path('create/', views.story_create_view, name='create'),
    
    # 스토리 보기: /stories/<username>/
    path('<str:username>/', views.story_view, name='view'),
    
    # 스토리 삭제: /stories/<pk>/delete/
    path('<int:pk>/delete/', views.story_delete_view, name='delete'),
]