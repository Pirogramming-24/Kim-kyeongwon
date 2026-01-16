from django.core.management.base import BaseCommand
from reviews.models import Movie
from reviews.tmdb_service import TMDBService
import time

class Command(BaseCommand):
    help = 'TMDB에서 인기 영화 데이터를 가져와 DB에 저장합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=2,
            help='가져올 페이지 수 (페이지당 약 20개 영화)',
        )

    def handle(self, *args, **options):
        pages = options['pages']
        tmdb_service = TMDBService()
        
        total_added = 0
        total_updated = 0
        
        self.stdout.write(self.style.SUCCESS(f'TMDB에서 {pages}페이지의 영화 데이터를 가져옵니다...'))
        
        for page in range(1, pages + 1):
            self.stdout.write(f'\n페이지 {page} 처리 중...')
            
            popular_movies = tmdb_service.get_popular_movies(page=page)
            
            if not popular_movies or 'results' not in popular_movies:
                self.stdout.write(self.style.ERROR(f'페이지 {page} 데이터를 가져올 수 없습니다.'))
                continue
            
            for movie_data in popular_movies['results']:
                try:
                    movie_id = movie_data['id']
                    details = tmdb_service.get_movie_details(movie_id)
                    credits = tmdb_service.get_movie_credits(movie_id)
                    
                    if not details:
                        continue
                    
                    parsed_data = tmdb_service.parse_movie_data(details, credits)
                    
                    movie, created = Movie.objects.update_or_create(
                        tmdb_id=parsed_data['tmdb_id'],
                        defaults=parsed_data
                    )
                    
                    if created:
                        total_added += 1
                        self.stdout.write(self.style.SUCCESS(f'✓ 추가: {movie.title}'))
                    else:
                        total_updated += 1
                        self.stdout.write(f'  업데이트: {movie.title}')
                    
                    time.sleep(0.3)
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ 오류 발생: {str(e)}'))
                    continue
        
        self.stdout.write(self.style.SUCCESS(f'\n\n완료!'))
        self.stdout.write(self.style.SUCCESS(f'새로 추가된 영화: {total_added}개'))
        self.stdout.write(self.style.SUCCESS(f'업데이트된 영화: {total_updated}개'))
        self.stdout.write(self.style.SUCCESS(f'총 영화 수: {Movie.objects.count()}개'))