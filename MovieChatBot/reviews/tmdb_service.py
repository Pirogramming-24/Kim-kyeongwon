import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        if not self.api_key:
            raise ValueError("TMDB_API_KEY가 .env 파일에 설정되지 않았습니다.")
    
    def _make_request(self, endpoint, params=None):
        """TMDB API 요청"""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        params['language'] = 'ko-KR'
        
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"TMDB API Error: {response.status_code}")
            return None
    
    def get_popular_movies(self, page=1):
        """인기 영화 목록 가져오기"""
        return self._make_request('/movie/popular', {'page': page})
    
    def get_movie_details(self, movie_id):
        """영화 상세 정보 가져오기"""
        return self._make_request(f'/movie/{movie_id}')
    
    def get_movie_credits(self, movie_id):
        """영화 출연진 및 제작진 정보 가져오기"""
        return self._make_request(f'/movie/{movie_id}/credits')
    
    def parse_movie_data(self, movie_data, credits_data=None):
        """TMDB 영화 데이터를 Django 모델 형식으로 파싱"""
        # 장르 정보 추출
        genres = [genre['name'] for genre in movie_data.get('genres', [])] if 'genres' in movie_data else []
        if not genres and 'genre_ids' in movie_data:
            genre_map = {
                28: '액션', 12: '모험', 16: '애니메이션', 35: '코미디', 80: '범죄',
                99: '다큐멘터리', 18: '드라마', 10751: '가족', 14: '판타지', 36: '역사',
                27: '공포', 10402: '음악', 9648: '미스터리', 10749: '로맨스', 878: 'SF',
                10770: 'TV 영화', 53: '스릴러', 10752: '전쟁', 37: '서부'
            }
            genres = [genre_map.get(gid, '기타') for gid in movie_data.get('genre_ids', [])]
        
        # 출연진 정보 추출
        cast_list = []
        director = ""
        
        if credits_data:
            cast_list = [actor['name'] for actor in credits_data.get('cast', [])[:5]]
            crew = credits_data.get('crew', [])
            directors = [member['name'] for member in crew if member.get('job') == 'Director']
            director = ', '.join(directors) if directors else ""
        
        release_date = movie_data.get('release_date')
        
        return {
            'tmdb_id': movie_data.get('id'),
            'title': movie_data.get('title', ''),
            'original_title': movie_data.get('original_title', ''),
            'director': director,
            'cast': ', '.join(cast_list),
            'genre': ', '.join(genres[:3]) if genres else '기타',
            'release_date': release_date if release_date else None,
            'runtime': movie_data.get('runtime'),
            'overview': movie_data.get('overview', ''),
            'poster_path': movie_data.get('poster_path', ''),
            'backdrop_path': movie_data.get('backdrop_path', ''),
            'vote_average': movie_data.get('vote_average', 0),
            'popularity': movie_data.get('popularity', 0),
        }