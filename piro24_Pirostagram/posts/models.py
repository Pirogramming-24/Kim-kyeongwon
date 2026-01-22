from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    """
    게시글 모델
    유저가 작성하는 게시글을 저장합니다
    """
    # 게시글 작성자 (User 모델과 외래키 관계)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 유저가 삭제되면 게시글도 삭제
        related_name='posts',  # user.posts.all()로 유저의 게시글 조회 가능
        verbose_name='작성자'
    )
    
    # 게시글 이미지
    image = models.ImageField(
        upload_to='posts/',  # 이미지 저장 경로
        verbose_name='이미지'
    )
    
    # 게시글 내용
    content = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name='내용'
    )
    
    # 생성 시간
    created_at = models.DateTimeField(
        auto_now_add=True,  # 생성될 때 자동으로 현재 시간 저장
        verbose_name='생성일시'
    )
    
    # 수정 시간
    updated_at = models.DateTimeField(
        auto_now=True,  # 수정될 때마다 자동으로 현재 시간 갱신
        verbose_name='수정일시'
    )
    
    # 좋아요 (다대다 관계)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',  # user.liked_posts.all()로 유저가 좋아요한 게시글 조회
        blank=True,
        verbose_name='좋아요'
    )
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글들'
        ordering = ['-created_at']  # 최신순으로 정렬
    
    def __str__(self):
        """객체를 문자열로 표현"""
        return f'{self.author.username}의 게시글 ({self.created_at.strftime("%Y-%m-%d")})'
    
    def get_likes_count(self):
        """좋아요 수를 반환"""
        return self.likes.count()
    
    def get_comments_count(self):
        """댓글 수를 반환"""
        return self.comments.count()

class Comment(models.Model):
    """
    댓글 모델
    게시글에 달리는 댓글을 저장합니다
    """
    # 댓글이 달린 게시글
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # 게시글이 삭제되면 댓글도 삭제
        related_name='comments',  # post.comments.all()로 게시글의 댓글 조회
        verbose_name='게시글'
    )
    
    # 댓글 작성자
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 유저가 삭제되면 댓글도 삭제
        related_name='comments',  # user.comments.all()로 유저의 댓글 조회
        verbose_name='작성자'
    )
    
    # 댓글 내용
    content = models.TextField(
        max_length=500,
        verbose_name='내용'
    )
    
    # 생성 시간
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일시'
    )
    
    # 수정 시간
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일시'
    )
    
    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글들'
        ordering = ['created_at']  # 오래된 순으로 정렬
    
    def __str__(self):
        """객체를 문자열로 표현"""
        return f'{self.author.username}의 댓글: {self.content[:20]}'