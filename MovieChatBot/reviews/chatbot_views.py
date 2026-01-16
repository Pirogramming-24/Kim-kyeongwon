from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from .chatbot_service import MovieChatbot
import json

def chatbot_page(request):
    """챗봇 페이지"""
    chatbot = MovieChatbot()
    suggestions = chatbot.get_quick_suggestions()
    
    context = {
        'suggestions': suggestions,
    }
    return render(request, 'chatbot.html', context)


def chatbot_api(request):
    """챗봇 API 엔드포인트"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': '메시지를 입력해주세요.'}, status=400)
            
            all_movies = Movie.objects.all()
            
            chatbot = MovieChatbot()
            response = chatbot.get_response(user_message, all_movies)
            
            return JsonResponse({
                'response': response,
                'success': True
            })
        
        except Exception as e:
            return JsonResponse({
                'error': f'오류가 발생했습니다: {str(e)}',
                'success': False
            }, status=500)
    
    return JsonResponse({'error': 'POST 요청만 가능합니다.'}, status=405)