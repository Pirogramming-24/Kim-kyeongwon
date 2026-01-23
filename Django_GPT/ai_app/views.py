from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import ChatHistory
from huggingface_hub import InferenceClient
import os

# Create your views here.
# Hugging Face Client 생성
def get_hf_client():
    api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    if not api_token:
        return None
    return InferenceClient(token=api_token)


# 홈 페이지
def home(request):
    return render(request, 'ai_app/home.html')


# 요약 탭 (공개 - 비로그인 허용)
def summarize(request):
    result = None
    error = None
    history = []
    
    if request.user.is_authenticated:
        history = ChatHistory.objects.filter(user=request.user, model_type='summarize')[:5]
    else:
        if request.method == 'GET':
            request.session['summarize_history'] = []
        history = request.session.get('summarize_history', [])[:5]
    
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        
        if input_text:
            try:
                client = get_hf_client()
                if not client:
                    error = "API 토큰이 설정되지 않았습니다."
                else:
                    response = client.summarization(
                        input_text,
                        model="facebook/bart-large-cnn"
                    )
                    
                    if isinstance(response, dict):
                        result = response.get('summary_text', '요약 결과를 가져올 수 없습니다.')
                    elif isinstance(response, str):
                        result = response
                    else:
                        result = str(response)
                    
                    if request.user.is_authenticated:
                        ChatHistory.objects.create(
                            user=request.user,
                            model_type='summarize',
                            input_text=input_text,
                            output_text=result
                        )
                        history = ChatHistory.objects.filter(user=request.user, model_type='summarize')[:5]
                    else:
                        session_history = request.session.get('summarize_history', [])
                        session_history.insert(0, {'input': input_text, 'output': result})
                        session_history = session_history[:5]
                        request.session['summarize_history'] = session_history
                        history = session_history
                        
            except Exception as e:
                error = f"모델 호출 실패: {str(e)}"
        else:
            error = "텍스트를 입력해주세요."
    
    return render(request, 'ai_app/summarize.html', {
        'result': result,
        'error': error,
        'history': history
    })


# 감정 분석 탭 (로그인 필요)
@login_required
def sentiment(request):
    result = None
    error = None
    history = ChatHistory.objects.filter(user=request.user, model_type='sentiment')[:5]
    
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        
        if input_text:
            try:
                client = get_hf_client()
                if not client:
                    error = "API 토큰이 설정되지 않았습니다."
                else:
                    response = client.text_classification(
                        input_text,
                        model="cardiffnlp/twitter-roberta-base-sentiment"
                    )
                    
                    if isinstance(response, list) and len(response) > 0:
                        sentiment_data = max(response, key=lambda x: x.get('score', 0))
                        label = sentiment_data.get('label', 'UNKNOWN')
                        score = sentiment_data.get('score', 0)
                        
                        label_map = {
                            'LABEL_0': 'NEGATIVE (부정)',
                            'LABEL_1': 'NEUTRAL (중립)',
                            'LABEL_2': 'POSITIVE (긍정)'
                        }
                        label_korean = label_map.get(label, label)
                        result = f"감정: {label_korean}, 확률: {score:.2%}"
                    else:
                        result = str(response)
                    
                    ChatHistory.objects.create(
                        user=request.user,
                        model_type='sentiment',
                        input_text=input_text,
                        output_text=result
                    )
                    history = ChatHistory.objects.filter(user=request.user, model_type='sentiment')[:5]
                    
            except Exception as e:
                error = f"모델 호출 실패: {str(e)}"
        else:
            error = "텍스트를 입력해주세요."
    
    return render(request, 'ai_app/sentiment.html', {
        'result': result,
        'error': error,
        'history': history
    })


# 번역 탭 (로그인 필요)
@login_required
def translate(request):
    result = None
    error = None
    history = ChatHistory.objects.filter(user=request.user, model_type='translate')[:5]
    
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        
        if input_text:
            try:
                client = get_hf_client()
                if not client:
                    error = "API 토큰이 설정되지 않았습니다."
                else:
                    # mBART 다국어 번역 모델 사용
                    response = client.translation(
                        input_text,
                        model="facebook/mbart-large-50-many-to-many-mmt",
                        src_lang="en_XX",  # 영어
                        tgt_lang="ko_KR"   # 한국어
                    )
                    
                    if isinstance(response, dict):
                        result = response.get('translation_text', '번역 결과를 가져올 수 없습니다.')
                    elif isinstance(response, str):
                        result = response
                    else:
                        result = str(response)
                    
                    ChatHistory.objects.create(
                        user=request.user,
                        model_type='translate',
                        input_text=input_text,
                        output_text=result
                    )
                    history = ChatHistory.objects.filter(user=request.user, model_type='translate')[:5]
                    
            except Exception as e:
                error = f"모델 호출 실패: {str(e)}"
        else:
            error = "텍스트를 입력해주세요."
    
    return render(request, 'ai_app/translate.html', {
        'result': result,
        'error': error,
        'history': history
    })

# 회원가입
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '회원가입이 완료되었습니다!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'ai_app/signup.html', {'form': form})


# 로그아웃
def logout_view(request):
    logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('home')