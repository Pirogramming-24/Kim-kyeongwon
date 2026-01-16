from django.db import models

# Create your models here.

# TMDB에서 가져온 영화 정보
class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, verbose_name='TMDB ID')
    title = models.CharField(max_length=300, verbose_name='영화 제목')
    original_title = models.CharField(max_length=300, verbose_name='원제', blank=True)
    director = models.CharField(max_length=200, verbose_name='감독', blank=True)
    cast = models.TextField(verbose_name='출연진', blank=True)
    genre = models.CharField(max_length=100, verbose_name='장르', blank=True)
    release_date = models.DateField(verbose_name='개봉일', null=True, blank=True)
    runtime = models.IntegerField(verbose_name='러닝타임(분)', null=True, blank=True)
    overview = models.TextField(verbose_name='줄거리', blank=True)
    poster_path = models.CharField(max_length=200, verbose_name='포스터 경로', blank=True)
    backdrop_path = models.CharField(max_length=200, verbose_name='배경 경로', blank=True)
    vote_average = models.FloatField(verbose_name='평점', default=0)
    popularity = models.FloatField(verbose_name='인기도', default=0)
    is_tmdb = models.BooleanField(default=True, verbose_name='TMDB 영화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self):
        return self.title
    
    def get_runtime_display(self):
        if not self.runtime:
            return "정보 없음"
        hours = self.runtime // 60
        minutes = self.runtime % 60
        if hours > 0:
            return f"{hours}시간 {minutes}분"
        return f"{minutes}분"
    
    def get_poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
    
    def get_backdrop_url(self):
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None
    
    class Meta:
        ordering = ['-created_at']


# 사용자가 작성한 리뷰
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

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, 
                            related_name='reviews', verbose_name='연결된 영화')
    
    # 직접 입력 필드
    title = models.CharField(max_length=300, verbose_name='영화 제목')
    director = models.CharField(max_length=100, verbose_name='감독', blank=True)
    main_actor = models.CharField(max_length=100, verbose_name='주연', blank=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name='장르')
    release_year = models.IntegerField(verbose_name='개봉 년도', null=True, blank=True)
    runtime = models.IntegerField(verbose_name='러닝타임(분)', null=True, blank=True)
    poster_image = models.ImageField(upload_to='posters/', verbose_name='포스터 이미지', null=True, blank=True)
    
    # 리뷰 내용
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='별점')
    content = models.TextField(verbose_name='리뷰 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    def __str__(self):
        return f"{self.title} - {self.rating}점"
    
    def get_runtime_display(self):
        runtime = self.runtime if self.runtime else (self.movie.runtime if self.movie else None)
        if not runtime:
            return "정보 없음"
        hours = runtime // 60
        minutes = runtime % 60
        if hours > 0:
            return f"{hours}시간 {minutes}분"
        return f"{minutes}분"
    
    def get_poster_url(self):
        """포스터 이미지 URL 가져오기"""
        if self.poster_image:
            return self.poster_image.url
        elif self.movie and self.movie.poster_path:
            return self.movie.get_poster_url()
        return None
    
    class Meta:
        ordering = ['-created_at']