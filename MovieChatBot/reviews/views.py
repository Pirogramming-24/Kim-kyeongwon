from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Value, FloatField
from django.db.models.functions import Coalesce, ExtractYear
from datetime import date
from .models import Movie, Review

# Create your views here.
def home(request):
    """메인 페이지 - 영화 목록 및 통계"""
    order_by = request.GET.get('order_by', '-created_at')
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '')
    
    # 통계 계산
    total_movies = Movie.objects.count()
    tmdb_movies = Movie.objects.filter(is_tmdb=True).count()
    user_reviews = Movie.objects.filter(is_tmdb=False).count()
    
    # 영화 목록 필터링
    movies = Movie.objects.all()
    
    if filter_type == 'tmdb':
        movies = movies.filter(is_tmdb=True)
    elif filter_type == 'user':
        movies = movies.filter(is_tmdb=False)
    
    # 검색 기능
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(director__icontains=search_query) |
            Q(cast__icontains=search_query) |
            Q(genre__icontains=search_query)
        )
    
    # 정렬
    if order_by == 'title':
        movies = movies.order_by('title')
    elif order_by == 'genre':
        movies = movies.order_by('genre', 'title')
    elif order_by == 'rating':
        # 사용자 리뷰 평점 기준으로 정렬
        movies = movies.annotate(
            user_rating=Coalesce(
                Avg('reviews__rating', output_field=FloatField()),
                Value(0.0, output_field=FloatField())
            )
        ).order_by('-user_rating', 'title')
    elif order_by == 'release_year':
        # release_date에서 년도 추출하여 정렬
        movies = movies.annotate(
            year=ExtractYear('release_date')
        ).order_by('-year', '-created_at')
    else:
        movies = movies.order_by('-created_at')
    
    # 페이지네이션
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_movies': total_movies,
        'tmdb_movies': tmdb_movies,
        'user_reviews': user_reviews,
        'current_order': order_by,
        'current_filter': filter_type,
        'search_query': search_query,
    }
    return render(request, 'movies_list.html', context)


def movies_detail(request, pk):
    """영화 상세 페이지"""
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return redirect('reviews:home')
    
    # 이 영화에 대한 리뷰
    review = movie.reviews.first()
    
    context = {
        'movie': movie,
        'review': review,
    }
    return render(request, 'movies_detail.html', context)

def reviews_create(request, movie_id=None):
    """리뷰 작성 페이지"""
    movie = None
    if movie_id:
        try:
            movie = Movie.objects.get(pk=movie_id)
            # 이미 리뷰가 있는지 확인
            existing_review = movie.reviews.first()
            if existing_review:
                # 이미 리뷰가 있으면 수정 페이지로 리다이렉트
                return redirect('reviews:reviews_update', pk=existing_review.pk)
        except Movie.DoesNotExist:
            return redirect('reviews:home')
    
    if request.method == 'POST':
        review = Review()
        
        # TMDB 영화 연결
        if movie_id and movie:
            review.movie = movie
            review.title = movie.title
            review.director = movie.director
            review.main_actor = movie.cast.split(',')[0].strip() if movie.cast else ''
            review.genre = movie.genre.split(',')[0].strip() if movie.genre else '기타'
            review.release_year = movie.release_date.year if movie.release_date else None
            review.runtime = movie.runtime
        else:
            # 직접 입력
            review.title = request.POST.get('title')
            review.director = request.POST.get('director')
            review.main_actor = request.POST.get('main_actor')
            review.genre = request.POST.get('genre')
            review.release_year = request.POST.get('release_year')
            review.runtime = request.POST.get('runtime')
            
            if request.FILES.get('poster_image'):
                review.poster_image = request.FILES.get('poster_image')
            
            # 사용자가 추가한 영화는 Movie 테이블에도 저장
            if review.title:
                # 같은 제목의 영화가 이미 있는지 확인
                existing_movie = Movie.objects.filter(
                    title=review.title,
                    is_tmdb=False
                ).first()
                
                if existing_movie:
                    # 이미 같은 영화가 있으면 해당 영화에 연결
                    review.movie = existing_movie
                    # 이미 리뷰가 있는지 확인
                    if existing_movie.reviews.exists():
                        return redirect('reviews:reviews_update', pk=existing_movie.reviews.first().pk)
                else:
                    # 새 영화 생성
                    # 사용자 추가 영화는 음수 tmdb_id 사용
                    last_user_movie = Movie.objects.filter(tmdb_id__lt=0).order_by('tmdb_id').first()
                    if last_user_movie:
                        new_tmdb_id = last_user_movie.tmdb_id - 1
                    else:
                        new_tmdb_id = -1
                    
                    # release_date 설정
                    release_date = None
                    if review.release_year:
                        try:
                            release_date = date(int(review.release_year), 1, 1)
                        except (ValueError, TypeError):
                            pass
                    
                    # poster_image 파일 가져오기
                    poster_file = request.FILES.get('poster_image')
                    
                    # Movie 객체 생성
                    user_movie = Movie.objects.create(
                        tmdb_id=new_tmdb_id,  # 고유한 음수 ID 사용
                        title=review.title,
                        director=review.director or "",
                        cast=review.main_actor or "",
                        genre=review.genre,
                        release_date=release_date,
                        runtime=int(review.runtime) if review.runtime else None,
                        is_tmdb=False,
                        overview=f"사용자가 추가한 영화입니다."
                    )
                    
                    # poster_image가 있으면 별도로 설정
                    if poster_file:
                        user_movie.poster_image = poster_file
                        user_movie.save()
                    
                    review.movie = user_movie
        
        review.rating = request.POST.get('rating')
        review.content = request.POST.get('content')
        review.save()
        
        # 리뷰가 연결된 영화 상세 페이지로 리다이렉트
        if review.movie:
            return redirect('reviews:movies_detail', pk=review.movie.pk)
        return redirect('reviews:home')
    
    context = {
        'movie': movie,
        'genre_choices': Review.GENRE_CHOICES,
        'rating_choices': Review.RATING_CHOICES,
    }
    return render(request, 'reviews_form.html', context)


def reviews_detail(request, pk):
    """리뷰 상세 페이지"""
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return redirect('reviews:home')
    
    context = {
        'review': review,
    }
    return render(request, 'reviews_detail.html', context)


def reviews_update(request, pk):
    """리뷰 수정 페이지"""
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return redirect('reviews:home')
    
    if request.method == 'POST':
        # TMDB 영화가 아닌 경우에만 영화 정보 수정 가능
        if not review.movie or not review.movie.is_tmdb:
            review.title = request.POST.get('title')
            review.director = request.POST.get('director')
            review.main_actor = request.POST.get('main_actor')
            review.genre = request.POST.get('genre')
            review.release_year = request.POST.get('release_year')
            review.runtime = request.POST.get('runtime')
            
            if request.FILES.get('poster_image'):
                review.poster_image = request.FILES.get('poster_image')
            
            # Movie의 정보도 업데이트
            if review.movie:
                review.movie.title = review.title
                review.movie.director = review.director or ""
                review.movie.cast = review.main_actor or ""
                review.movie.genre = review.genre
                review.movie.runtime = review.runtime if review.runtime else None
                
                # release_date 업데이트
                if review.release_year:
                    try:
                        review.movie.release_date = date(int(review.release_year), 1, 1)
                    except (ValueError, TypeError):
                        pass
                
                if request.FILES.get('poster_image'):
                    review.movie.poster_image = request.FILES.get('poster_image')
                
                review.movie.save()
        
        review.rating = request.POST.get('rating')
        review.content = request.POST.get('content')
        review.save()
        
        # 리뷰 수정 후 영화 상세 페이지로 리다이렉트
        if review.movie:
            return redirect('reviews:movies_detail', pk=review.movie.pk)
        return redirect('reviews:reviews_detail', pk=review.pk)
    
    context = {
        'review': review,
        'genre_choices': Review.GENRE_CHOICES,
        'rating_choices': Review.RATING_CHOICES,
    }
    return render(request, 'reviews_form.html', context)


def reviews_delete(request, pk):
    """리뷰 삭제"""
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return redirect('reviews:home')
    
    if request.method == 'POST':
        movie_pk = review.movie.pk if review.movie else None
        
        # Review만 삭제
        review.delete()
        
        # 리뷰가 연결된 영화가 있으면 해당 영화 상세 페이지로, 없으면 홈으로
        if movie_pk:
            return redirect('reviews:movies_detail', pk=movie_pk)
        return redirect('reviews:home')
    
    return redirect('reviews:reviews_detail', pk=pk)


def search_movies(request):
    """영화 검색"""
    query = request.GET.get('q', '')
    movies = []
    
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(cast__icontains=query)
        )
    
    context = {
        'movies': movies,
        'query': query,
    }
    return render(request, 'search_results.html', context)