from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
@login_required
def feed_view(request):
    """
    피드 뷰 (메인 화면)
    로그인한 유저가 팔로우하는 사람들의 게시글을 보여줌
    """
    # 내가 팔로우하는 사람들의 게시글 + 내 게시글
    following_users = request.user.following.all()
    posts = Post.objects.filter(
        author__in=following_users
    ) | Post.objects.filter(author=request.user)
    
    posts = posts.distinct()
    
    # 정렬 기준
    sort = request.GET.get('sort', 'latest')
    
    if sort == 'likes':
        # 좋아요 많은 순
        posts = posts.annotate(likes_count=Count('likes')).order_by('-likes_count', '-created_at')
    else:
        # 최신순 (기본)
        posts = posts.order_by('-created_at')
    
    # 댓글 폼
    comment_form = CommentForm()
    
    context = {
        'posts': posts,
        'comment_form': comment_form,
        'current_sort': sort,
    }
    
    return render(request, 'posts/feed.html', context)

@login_required
def post_create_view(request):
    """
    게시글 작성 뷰
    GET: 게시글 작성 폼을 보여줌
    POST: 폼 데이터를 받아서 새 게시글 생성
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # 아직 DB에 저장하지 않음
            post.author = request.user  # 작성자를 현재 로그인한 유저로 설정
            post.save()  # DB에 저장
            messages.success(request, '게시글이 작성되었습니다!')
            return redirect('posts:feed')
    else:
        form = PostForm()
    
    return render(request, 'posts/post_form.html', {'form': form, 'title': '게시글 만들기'})

@login_required
def post_detail_view(request, pk):
    """
    게시글 상세 뷰
    특정 게시글과 그 댓글들을 보여줌
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_update_view(request, pk):
    """
    게시글 수정 뷰
    GET: 수정 폼을 보여줌
    POST: 폼 데이터를 받아서 게시글 수정
    """
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자만 수정 가능
    if post.author != request.user:
        messages.error(request, '게시글 작성자만 수정할 수 있습니다.')
        return redirect('posts:detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '게시글이 수정되었습니다!')
            return redirect('posts:detail', pk=pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': '게시글 수정',
        'is_update': True
    })

@login_required
def post_delete_view(request, pk):
    """
    게시글 삭제 뷰
    작성자만 삭제 가능
    """
    post = get_object_or_404(Post, pk=pk)
    
    # 작성자만 삭제 가능
    if post.author != request.user:
        messages.error(request, '게시글 작성자만 삭제할 수 있습니다.')
        return redirect('posts:detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, '게시글이 삭제되었습니다!')
        return redirect('posts:feed')
    
    return render(request, 'posts/post_delete.html', {'post': post})

@login_required
def like_toggle_view(request, pk):
    """
    좋아요 토글 뷰
    게시글에 좋아요를 누르거나 취소함
    Ajax로 처리되어 페이지 새로고침 없이 동작
    """
    post = get_object_or_404(Post, pk=pk)
    
    # 이미 좋아요를 눌렀으면 취소, 아니면 좋아요
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    
    # Ajax 요청이면 JSON 응답
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_liked': is_liked,
            'likes_count': post.get_likes_count(),
        })
    
    # 일반 요청이면 이전 페이지로 리다이렉트
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))

@login_required
def comment_create_view(request, pk):
    """
    댓글 작성 뷰
    특정 게시글에 댓글 추가
    """
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '댓글이 작성되었습니다!')
    
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))

@login_required
def comment_update_view(request, pk):
    """
    댓글 수정 뷰
    """
    comment = get_object_or_404(Comment, pk=pk)
    
    # 작성자만 수정 가능
    if comment.author != request.user:
        messages.error(request, '댓글 작성자만 수정할 수 있습니다.')
        return redirect('posts:detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, '댓글이 수정되었습니다!')
            return redirect('posts:detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
    }
    
    return render(request, 'posts/comment_form.html', context)

@login_required
def comment_delete_view(request, pk):
    """
    댓글 삭제 뷰
    """
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    
    # 작성자만 삭제 가능
    if comment.author != request.user:
        messages.error(request, '댓글 작성자만 삭제할 수 있습니다.')
    else:
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다!')
    
    return redirect('posts:detail', pk=post_pk)