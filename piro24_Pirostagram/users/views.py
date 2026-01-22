from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import User
from .forms import SignUpForm, LoginForm, ProfileUpdateForm

# Create your views here.
def signup_view(request):
    """
    회원가입 뷰
    GET: 회원가입 폼을 보여줌
    POST: 폼 데이터를 받아서 새 유저를 생성
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # 새 유저 생성
            login(request, user)  # 자동 로그인
            messages.success(request, '회원가입이 완료되었습니다!')
            return redirect('posts:feed')  # 피드로 이동
    else:
        form = SignUpForm()
    
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    """
    로그인 뷰
    GET: 로그인 폼을 보여줌
    POST: 폼 데이터를 받아서 로그인 처리
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'{user.username}님, 환영합니다!')
            
            # 다음에 가야할 페이지가 있으면 그곳으로, 없으면 피드로
            next_url = request.GET.get('next', 'posts:feed')
            return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    로그아웃 뷰
    로그인된 유저를 로그아웃 시킴
    """
    logout(request)
    messages.success(request, '로그아웃 되었습니다.')
    return redirect('users:login')

@login_required
def profile_view(request, username):
    """
    프로필 조회 뷰
    특정 유저의 프로필 페이지를 보여줌
    """
    # username으로 유저 찾기 (없으면 404 에러)
    user = get_object_or_404(User, username=username)
    
    # 해당 유저의 게시글들 가져오기 (최신순)
    posts = user.posts.all().order_by('-created_at')
    
    # 현재 로그인한 유저가 이 프로필 유저를 팔로우하고 있는지 확인
    is_following = request.user.following.filter(id=user.id).exists()
    
    context = {
        'profile_user': user,  # 프로필 주인
        'posts': posts,
        'is_following': is_following,
        'is_own_profile': request.user == user,  # 자기 프로필인지 확인
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def profile_update_view(request):
    """
    프로필 수정 뷰
    GET: 프로필 수정 폼을 보여줌
    POST: 폼 데이터를 받아서 프로필 수정
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필이 수정되었습니다!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/profile_update.html', {'form': form})

@login_required
def user_search_view(request):
    """
    유저 검색 뷰
    검색어로 유저를 찾아서 결과를 보여줌
    """
    query = request.GET.get('q', '')  # 검색어 가져오기
    users = []
    
    if query:
        # username 또는 first_name 또는 last_name에 검색어가 포함된 유저 찾기
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)  # 본인은 제외
    
    context = {
        'users': users,
        'query': query,
    }
    
    return render(request, 'users/search.html', context)

@login_required
def follow_toggle_view(request, username):
    """
    팔로우/언팔로우 토글 뷰
    특정 유저를 팔로우하거나 언팔로우함
    Ajax로 처리되어 페이지 새로고침 없이 동작
    """
    # 팔로우할 유저 찾기
    user_to_follow = get_object_or_404(User, username=username)
    
    # 자기 자신은 팔로우할 수 없음
    if request.user == user_to_follow:
        messages.error(request, '자기 자신은 팔로우할 수 없습니다.')
        return redirect('users:profile', username=username)
    
    # 이미 팔로우 중이면 언팔로우, 아니면 팔로우
    if request.user.following.filter(id=user_to_follow.id).exists():
        request.user.following.remove(user_to_follow)
        is_following = False
        messages.success(request, f'{user_to_follow.username}님을 언팔로우했습니다.')
    else:
        request.user.following.add(user_to_follow)
        is_following = True
        messages.success(request, f'{user_to_follow.username}님을 팔로우했습니다.')
    
    # Ajax 요청이면 JSON 응답
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'followers_count': user_to_follow.get_followers_count(),
        })
    
    # 일반 요청이면 프로필 페이지로 리다이렉트
    return redirect('users:profile', username=username)

@login_required
def followers_list_view(request, username):
    """
    팔로워 목록 뷰
    특정 유저의 팔로워들을 보여줌
    """
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    
    context = {
        'profile_user': user,
        'users': followers,
        'list_type': 'followers',
    }
    
    return render(request, 'users/follow_list.html', context)

@login_required
def following_list_view(request, username):
    """
    팔로잉 목록 뷰
    특정 유저가 팔로우하는 사람들을 보여줌
    """
    user = get_object_or_404(User, username=username)
    following = user.following.all()
    
    context = {
        'profile_user': user,
        'users': following,
        'list_type': 'following',
    }
    
    return render(request, 'users/follow_list.html', context)