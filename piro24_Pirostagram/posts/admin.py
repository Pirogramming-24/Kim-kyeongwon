from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """게시글 관리자 설정"""
    list_display = ['author', 'content_preview', 'created_at', 'get_likes_count']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']
    
    def content_preview(self, obj):
        """내용 미리보기 (처음 30자만)"""
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_preview.short_description = '내용'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """댓글 관리자 설정"""
    list_display = ['author', 'post', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']
    
    def content_preview(self, obj):
        """내용 미리보기 (처음 30자만)"""
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_preview.short_description = '내용'