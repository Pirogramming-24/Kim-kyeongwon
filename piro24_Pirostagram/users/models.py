from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    커스텀 유저 모델
    Django의 기본 User 모델을 상속받아 추가 필드를 정의합니다
    """
    # 프로필 이미지 (선택사항)
    profile_image = models.ImageField(
        upload_to='profile_pics/',  # 프로필 이미지 저장 경로
        blank=True,  # 빈 값 허용
        null=True  # NULL 값 허용
    )
    
    # 자기소개
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='소개'
    )
    
    # 팔로우 관계 (다대다 관계)
    # 한 유저는 여러 명을 팔로우할 수 있고, 여러 명에게 팔로우될 수 있습니다
    following = models.ManyToManyField(
        'self',  # 자기 자신(User)을 참조
        symmetrical=False,  # 비대칭 관계 (A가 B를 팔로우해도 B가 A를 팔로우하는 것은 아님)
        related_name='followers',  # 역참조 이름 (user.followers.all()로 팔로워 목록 조회)
        blank=True
    )
    
    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
    
    def __str__(self):
        """객체를 문자열로 표현할 때 사용"""
        return self.username
    
    def get_followers_count(self):
        """팔로워 수를 반환"""
        return self.followers.count()
    
    def get_following_count(self):
        """팔로잉 수를 반환"""
        return self.following.count()
    
    def get_posts_count(self):
        """게시글 수를 반환"""
        return self.posts.count()