from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # 피드 (메인 화면): /posts/
    path('', views.feed_view, name='feed'),
    
    # 게시글 작성: /posts/create/
    path('create/', views.post_create_view, name='create'),
    
    # 게시글 상세: /posts/<pk>/
    path('<int:pk>/', views.post_detail_view, name='detail'),
    
    # 게시글 수정: /posts/<pk>/update/
    path('<int:pk>/update/', views.post_update_view, name='update'),
    
    # 게시글 삭제: /posts/<pk>/delete/
    path('<int:pk>/delete/', views.post_delete_view, name='delete'),
    
    # 좋아요 토글: /posts/<pk>/like/
    path('<int:pk>/like/', views.like_toggle_view, name='like_toggle'),
    
    # 댓글 작성: /posts/<pk>/comment/
    path('<int:pk>/comment/', views.comment_create_view, name='comment_create'),
    
    # 댓글 수정: /posts/comment/<pk>/update/
    path('comment/<int:pk>/update/', views.comment_update_view, name='comment_update'),
    
    # 댓글 삭제: /posts/comment/<pk>/delete/
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
]