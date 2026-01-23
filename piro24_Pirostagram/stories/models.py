from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Story(models.Model):
    """
    스토리 모델
    유저가 올리는 스토리를 저장합니다
    스토리는 24시간 후 자동으로 만료됩니다
    """
    # 스토리 작성자
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories',
        verbose_name='작성자'
    )
    
    # 생성 시간
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일시'
    )
    
    class Meta:
        verbose_name = '스토리'
        verbose_name_plural = '스토리들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.author.username}의 스토리 ({self.created_at.strftime("%Y-%m-%d %H:%M")})'
    
    def is_expired(self):
        """스토리가 만료되었는지 확인 (24시간 경과)"""
        return timezone.now() > self.created_at + timedelta(hours=24)
    
    def get_images_count(self):
        """스토리에 포함된 이미지 수를 반환"""
        return self.images.count()

class StoryImage(models.Model):
    """
    스토리 이미지 모델
    하나의 스토리는 여러 장의 이미지를 가질 수 있습니다
    """
    # 이 이미지가 속한 스토리
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='스토리'
    )
    
    # 이미지 파일
    image = models.ImageField(
        upload_to='stories/',
        verbose_name='이미지'
    )
    
    # 순서 (여러 이미지를 순서대로 보여주기 위함)
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='순서'
    )
    
    # 생성 시간
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일시'
    )
    
    class Meta:
        verbose_name = '스토리 이미지'
        verbose_name_plural = '스토리 이미지들'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f'{self.story.author.username}의 스토리 이미지 {self.order + 1}'