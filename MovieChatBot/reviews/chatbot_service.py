import os
from openai import OpenAI
from dotenv import load_dotenv
from django.db.models import Q

load_dotenv()

class MovieChatbot:
    def __init__(self):
        self.api_key = os.getenv('UPSTAGE_API_KEY')
        if not self.api_key:
            raise ValueError("UPSTAGE_API_KEY가 .env 파일에 설정되지 않았습니다.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.upstage.ai/v1/solar"
        )
    
    def get_movie_context(self, movies):
        """영화 데이터를 컨텍스트로 변환"""
        context = "현재 데이터베이스에 저장된 영화 목록:\n\n"
        
        for i, movie in enumerate(movies, 1):
            context += f"{i}. 제목: {movie.title}\n"
            if movie.director:
                context += f"   감독: {movie.director}\n"
            if movie.cast:
                context += f"   출연: {movie.cast}\n"
            if movie.genre:
                context += f"   장르: {movie.genre}\n"
            if movie.release_date:
                context += f"   개봉: {movie.release_date.year}년\n"
            if movie.overview:
                context += f"   줄거리: {movie.overview[:100]}...\n"
            if movie.vote_average:
                context += f"   평점: {movie.vote_average}/10\n"
            context += "\n"
        
        return context
    
    def search_relevant_movies(self, query, all_movies):
        """쿼리와 관련된 영화 검색"""
        keywords = query.split()
        relevant_movies = set()
        
        for keyword in keywords:
            movies = all_movies.filter(
                Q(title__icontains=keyword) |
                Q(director__icontains=keyword) |
                Q(cast__icontains=keyword) |
                Q(genre__icontains=keyword) |
                Q(overview__icontains=keyword)
            )
            relevant_movies.update(movies)
        
        if not relevant_movies:
            return list(all_movies.order_by('-popularity')[:10])
        
        return list(relevant_movies)[:10]
    
    def get_response(self, user_message, all_movies):
        """사용자 메시지에 대한 AI 응답 생성"""
        relevant_movies = self.search_relevant_movies(user_message, all_movies)
        movie_context = self.get_movie_context(relevant_movies)
        
        system_prompt = f"""당신은 영화 추천 전문가입니다. 
사용자의 질문에 대해 데이터베이스에 있는 영화 정보를 바탕으로 친절하고 상세하게 답변해주세요.
영화를 추천할 때는 이유와 함께 추천해주세요.

{movie_context}

답변 가이드라인:
1. 사용자가 특정 장르나 감독을 언급하면 해당 영화를 우선 추천
2. 영화 제목, 감독, 주연 배우, 장르, 줄거리를 포함하여 설명
3. 2-3개 정도의 영화를 추천하되, 각 영화의 특징을 명확히 설명
4. 친근하고 자연스러운 대화체 사용
5. 한국어로 답변"""
        
        try:
            response = self.client.chat.completions.create(
                model="solar-pro",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    def get_quick_suggestions(self):
        """빠른 질문 제안"""
        return [
            "액션 영화 추천해줘",
            "로맨스 영화 추천",
            "고평점 영화 보여줘",
            "최근 영화 추천"
        ]