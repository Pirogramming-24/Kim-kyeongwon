from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Story, StoryImage
from .forms import StoryImageForm
from users.models import User

# Create your views here.
@login_required
def story_list_view(request):
    """
    스토리 목록 뷰
    팔로우하는 사람들의 활성 스토리 목록을 보여줌
    """
    # 24시간 이내의 스토리만 표시
    time_threshold = timezone.now() - timedelta(hours=24)
    
    # 내가 팔로우하는 사람들 + 나 자신
    following_users = list(request.user.following.all()) + [request.user]
    
    # 각 유저의 최신 스토리 가져오기 (24시간 이내)
    stories = []
    for user in following_users:
        user_stories = Story.objects.filter(
            author=user,
            created_at__gte=time_threshold
        ).order_by('-created_at')
        
        if user_stories.exists():
            stories.append({
                'user': user,
                'story': user_stories.first(),
                'count': user_stories.count()
            })
    
    context = {
        'stories': stories,
    }
    
    return render(request, 'stories/story_list.html', context)


@login_required
def story_create_view(request):
    """
    스토리 생성 뷰
    한 장의 이미지를 업로드하여 새 스토리 생성
    """
    if request.method == 'POST':
        form = StoryImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            # 새 스토리 생성 (이미지 1장당 1개의 스토리)
            story = Story.objects.create(author=request.user)
            
            # 스토리에 이미지 추가
            StoryImage.objects.create(
                story=story,
                image=form.cleaned_data['image'],
                order=0
            )
            
            messages.success(request, '스토리가 생성되었습니다!')
            return redirect('posts:feed')
    else:
        form = StoryImageForm()
    
    return render(request, 'stories/story_form.html', {'form': form})


@login_required
def story_view(request, username):
    """
    특정 유저의 스토리 보기 (여러 스토리 자동 재생)
    """
    user = get_object_or_404(User, username=username)
    
    # 24시간 이내의 스토리만
    time_threshold = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(
        author=user,
        created_at__gte=time_threshold
    ).order_by('-created_at')
    
    if not stories.exists():
        messages.info(request, f'{username}님의 활성 스토리가 없습니다.')
        return redirect('posts:feed')
    
    # 모든 스토리의 이미지들을 순서대로 수집
    all_images = []
    for story in stories:
        for image in story.images.all():
            all_images.append({
                'url': image.image.url,
                'story': story,
            })
    
    context = {
        'story_user': user,
        'images': all_images,
        'total_stories': stories.count(),
    }
    
    return render(request, 'stories/story_view.html', context)


@login_required
def story_delete_view(request, pk):
    """
    스토리 삭제 뷰
    """
    story = get_object_or_404(Story, pk=pk)
    
    # 작성자만 삭제 가능
    if story.author != request.user:
        messages.error(request, '스토리 작성자만 삭제할 수 있습니다.')
        return redirect('posts:feed')
    
    if request.method == 'POST':
        story.delete()
        messages.success(request, '스토리가 삭제되었습니다!')
        return redirect('posts:feed')
    
    return render(request, 'stories/story_delete.html', {'story': story})