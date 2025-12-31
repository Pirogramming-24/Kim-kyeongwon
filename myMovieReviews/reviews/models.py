from django.db import models

# Create your models here.
class Review(models.Model):
    GENRE_CHOICES = [
        ('액션', '액션'),
        ('코미디', '코미디'),
        ('드라마', '드라마'),
        ('로맨스', '로맨스'),
        ('스릴러', '스릴러'),
        ('공포', '공포'),
        ('SF', 'SF'),
        ('판타지', '판타지'),
        ('범죄', '범죄'),
        ('애니메이션', '애니메이션'),
        ('다큐멘터리', '다큐멘터리'),
        ('기타', '기타'),
    ]
    
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    title = models.CharField(max_length=300, verbose_name='영화 제목')
    director = models.CharField(max_length=100, verbose_name='감독')
    main_actor = models.CharField(max_length=100, verbose_name='주연')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name='장르')
    release_year = models.IntegerField(verbose_name='개봉 년도')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='별점')
    runtime = models.IntegerField(verbose_name='러닝타임(분)')
    content = models.TextField(verbose_name='리뷰 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    
    def __str__(self):
        return self.title
    
    def get_runtime_display(self):
        """러닝타임을 시간 단위로 변환"""
        hours = self.runtime // 60
        minutes = self.runtime % 60
        if hours > 0:
            return f"{hours}시간 {minutes}분"
        return f"{minutes}분"