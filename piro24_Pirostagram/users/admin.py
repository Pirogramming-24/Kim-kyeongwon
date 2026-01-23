from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User 모델을 관리자 페이지에 등록"""
    
    # 관리자 페이지의 리스트 화면에 표시할 필드
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    
    # 기본 UserAdmin 필드에 우리가 추가한 필드들을 포함
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('profile_image', 'bio', 'following')}),
    )