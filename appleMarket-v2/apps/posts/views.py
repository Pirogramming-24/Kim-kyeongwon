from django.shortcuts import render, redirect
from .forms import PostForm, NutritionForm
from .models import NutritionInfo, Post
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .services.ocr_service import run_ocr
from .services.rules import extract_nutrition

# Create your views here.
def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_txt:
        posts = posts.filter(title__icontains=search_txt)  # 대소문자 구분 없이 검색
    
    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except (ValueError, TypeError):
        pass  # 필터를 무시하되, 기존 검색 필터를 유지

    context = {
        'posts': posts,
        'search_txt': search_txt,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'posts/list.html', context=context)

def create(request):
    if request.method == 'GET':
        post_form = PostForm()
        nutrition_form = NutritionForm()
        return render(request, 'posts/create.html', {
            'post_form': post_form,
            'nutrition_form': nutrition_form,
        })
    else:
        post_form = PostForm(request.POST, request.FILES)
        nutrition_form = NutritionForm(request.POST)

        if post_form.is_valid() and nutrition_form.is_valid():
            post = post_form.save()

            nutrition = nutrition_form.save(commit=False)
            nutrition.post = post
            nutrition.save()

            return redirect('/')

        return render(request, 'posts/create.html', {
            'post_form': post_form,
            'nutrition_form': nutrition_form,
        })

def detail(request, pk):
    target_post = Post.objects.get(id = pk)
    context = { 'post': target_post }
    return render(request, 'posts/detail.html', context=context)

def update(request, pk):
    post = Post.objects.get(id=pk)
    nutrition = getattr(post, "nutrition", None)

    if request.method == 'GET':
        post_form = PostForm(instance=post)
        nutrition_form = NutritionForm(instance=nutrition)

        return render(request, 'posts/update.html', {
            'post_form': post_form,
            'nutrition_form': nutrition_form,
            'post': post,
        })

    # POST
    post_form = PostForm(request.POST, request.FILES, instance=post)
    nutrition_form = NutritionForm(request.POST, instance=nutrition)

    if post_form.is_valid() and nutrition_form.is_valid():
        post_form.save()

        n = nutrition_form.save(commit=False)
        n.post = post
        n.save()

        return redirect('posts:detail', pk=pk)

    return render(request, 'posts/update.html', {
        'post_form': post_form,
        'nutrition_form': nutrition_form,
        'post': post,
    })


def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')

@require_POST
@csrf_exempt
def ocr_preview(request):
    """영양 성분표 OCR 미리보기"""

    # 기본 결과
    empty_result = {
        "calories_kcal": None,
        "carbs_g": None,
        "protein_g": None,
        "fat_g": None,
    }

    try:
        f = request.FILES.get("nutrition_image")
        if not f:
            return JsonResponse({
                "ok": True,
                "nutrition": empty_result
            })

        # 파일 검증
        if f.size > 10 * 1024 * 1024:
            return JsonResponse({
                "ok": True,
                "nutrition": empty_result
            })

        if f.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            return JsonResponse({
                "ok": True,
                "nutrition": empty_result
            })

        file_bytes = f.read()

        # OCR 실행
        lines = run_ocr(file_bytes)
        if not lines:
            return JsonResponse({
                "ok": True,
                "nutrition": empty_result
            })

        nutrition = extract_nutrition(lines)

        return JsonResponse({
            "ok": True,
            "nutrition": nutrition
        })

    except Exception as e:
        print("OCR preview error:", e)
        return JsonResponse({
            "ok": True,
            "nutrition": empty_result
        })