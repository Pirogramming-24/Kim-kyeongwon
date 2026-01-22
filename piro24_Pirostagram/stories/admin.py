from django.contrib import admin
from .models import Story, StoryImage

# Register your models here.
class StoryImageInline(admin.TabularInline):
    """스토리 관리 페이지에서 이미지를 함께 관리"""
    model = StoryImage
    extra = 1

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    """스토리 관리자 설정"""
    list_display = ['author', 'created_at', 'get_images_count', 'is_expired']
    list_filter = ['created_at']
    search_fields = ['author__username']
    inlines = [StoryImageInline]

@admin.register(StoryImage)
class StoryImageAdmin(admin.ModelAdmin):
    """스토리 이미지 관리자 설정"""
    list_display = ['story', 'order', 'created_at']
    list_filter = ['created_at']