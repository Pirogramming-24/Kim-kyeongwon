from django.shortcuts import render, redirect
from .models import Review

# Create your views here.
def reviews_list(request):
    """리뷰 리스트 페이지"""
    order_by = request.GET.get('order_by', '-created_at') # 정렬 기능 추가
    
    if order_by == 'title':
        review = Review.objects.all().order_by('title')
    elif order_by == 'rating':
        review = Review.objects.all().order_by('-rating', 'title')
    elif order_by == 'release_year':
        review = Review.objects.all().order_by('-release_year')
    else:
        review = Review.objects.all().order_by('-created_at')
    
    context = {
        'reviews': review,
        'current_order': order_by,
    }
    return render(request, 'reviews_list.html', context)

def reviews_detail(request, pk):
    """리뷰 디테일 페이지"""
    review = Review.objects.get(pk=pk)
    context = {
        'review': review,
    }
    return render(request, 'reviews_detail.html', context)

def reviews_create(request):
    """리뷰 작성 페이지"""
    if request.method == 'POST':
        review = Review()
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.main_actor = request.POST.get('main_actor')
        review.genre = request.POST.get('genre')
        review.release_year = request.POST.get('release_year')
        review.rating = request.POST.get('rating')
        review.runtime = request.POST.get('runtime')
        review.content = request.POST.get('content')
        review.save()
        return redirect('reviews:reviews_list')
    
    context = {
        'genre_choices': Review.GENRE_CHOICES,
        'rating_choices': Review.RATING_CHOICES,
    }
    return render(request, 'reviews_form.html', context)

def reviews_update(request, pk):
    """리뷰 수정 페이지"""
    review = Review.objects.get(pk=pk)
    
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.main_actor = request.POST.get('main_actor')
        review.genre = request.POST.get('genre')
        review.release_year = request.POST.get('release_year')
        review.rating = request.POST.get('rating')
        review.runtime = request.POST.get('runtime')
        review.content = request.POST.get('content')
        review.save()
        return redirect('reviews:reviews_detail', pk=review.pk)
    
    context = {
        'review': review,
        'genre_choices': Review.GENRE_CHOICES,
        'rating_choices': Review.RATING_CHOICES,
    }
    return render(request, 'reviews_form.html', context)

def reviews_delete(request, pk):
    """리뷰 삭제"""
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:reviews_list')
    return redirect('reviews:reviews_detail', pk=pk)