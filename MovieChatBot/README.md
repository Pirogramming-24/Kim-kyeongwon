# 🎬 My Movie Reviews

## ✨ 주요 기능

### 1. 영화 관리
- TMDB API를 통한 인기 영화 자동 수집 (약 40개)
- 사용자가 직접 영화 추가 가능
- 영화 목록 페이지 (포스터 카드 레이아웃)
- 영화 상세 페이지 (포스터, 배경 이미지, 영화 정보)
- 통계 대시보드 (총 영화 수, TMDB 영화, 직접 추가)

### 2. 리뷰 시스템
- 영화당 하나의 리뷰 작성 가능
- 리뷰 작성, 수정, 삭제 (CRUD)
- 1~5점 별점 시스템
- 포스터 이미지 업로드

### 3. 검색 및 정렬
- 영화 제목, 감독, 배우 기준 검색
- 최신순, 제목순, 장르별, 평점별, 개봉년도별 정렬
- 필터링 (전체 / TMDB / 직접 추가)
- 페이지네이션 (12개씩)

### 4. AI 챗봇 (RAG 시스템)
- Upstage Solar LLM 연동
- 영화 추천 및 정보 제공
- 실시간 채팅 인터페이스
- 빠른 질문 버튼

### 5. UI/UX
- 보라색 그라데이션 디자인
- 반응형 디자인 (모바일, 태블릿, 데스크톱)
- 부드러운 애니메이션 효과

## 📦 설치 및 실행 방법

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd MovieChatBot
```

### 2. 가상환경 생성 및 활성화
```bash
# Windows
python -m venv venv
source venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력:
```env
# TMDB API Key
TMDB_API_KEY=your_tmdb_api_key_here

# Upstage API Key
UPSTAGE_API_KEY=your_upstage_api_key_here
```

**API 키 발급 방법:**
- **TMDB API**: [https://developer.themoviedb.org/](https://developer.themoviedb.org/)에서 회원가입 후 API 키 발급
- **Upstage API**: [https://console.upstage.ai/](https://console.upstage.ai/)에서 회원가입 후 API 키 발급

### 5. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. TMDB 영화 데이터 수집
```bash
# 2페이지(약 40개)의 인기 영화 데이터 수집
python manage.py fetch_tmdb_movies --pages 2
```

페이지 수를 조절하여 원하는 만큼 영화 수집 가능:
```bash
# 1페이지(약 20개)
python manage.py fetch_tmdb_movies --pages 1

# 5페이지(약 100개)
python manage.py fetch_tmdb_movies --pages 5
```

### 7. 개발 서버 실행
```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 접속

## 📁 프로젝트 구조
```
MovieChatBot/
├── config/                     # Django 프로젝트 설정
│   ├── settings.py             # 프로젝트 설정
│   ├── urls.py                 # 메인 URL 설정
│   └── wsgi.py
│
├── reviews/                    # 메인 앱
│   ├── management/
│   │   └── commands/
│   │       └── fetch_tmdb_movies.py  # TMDB 데이터 수집 커맨드
│   │
│   ├── templates/              # HTML 템플릿
│   │   ├── base.html
│   │   ├── movies_list.html
│   │   ├── movies_detail.html
│   │   ├── reviews_form.html
│   │   ├── reviews_detail.html
│   │   └── chatbot.html
│   │
│   ├── models.py               # Movie, Review 모델
│   ├── views.py                # 영화/리뷰 뷰
│   ├── chatbot_views.py        # 챗봇 뷰
│   ├── urls.py                 # 앱 URL 설정
│   ├── tmdb_service.py         # TMDB API 서비스
│   ├── chatbot_service.py      # AI 챗봇 서비스
│   └── admin.py                # Django 관리자 설정
│
├── media/                      # 업로드된 파일 (자동 생성)
│   └── posters/                # 포스터 이미지
│
├── manage.py
├── requirements.txt
├── .env                        # 환경 변수 (직접 생성)
├── .env.example                # 환경 변수 템플릿
├── .gitignore
└── README.md
```
