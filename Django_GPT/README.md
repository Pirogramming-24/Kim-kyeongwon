# 나만의 AI 사이트 (Django)

Django와 Hugging Face API를 활용한 AI 웹 서비스입니다.

---

## 사용 모델 (3개 이상)

### 1. facebook/bart-large-cnn
- **태스크**: Summarization (요약)
- **설명**: 긴 텍스트를 짧고 간결하게 요약하는 BART 기반 모델입니다.
- **입력 예시**:
```
  The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. 
  It is named after the engineer Gustave Eiffel, whose company designed and built the tower. 
  Constructed from 1887 to 1889 as the entrance to the 1889 World's Fair, it was initially 
  criticized by some of France's leading artists and intellectuals for its design, but it has 
  become a global cultural icon of France and one of the most recognizable structures in the world.
```
- **출력 예시**:
```
  The Eiffel Tower is a wrought-iron lattice tower in Paris, France. It was built from 1887 
  to 1889 as the entrance to the 1889 World's Fair and has become a global cultural icon.
```
- **실행 화면 예시**:
  1. 홈페이지에서 "요약" 탭 클릭
  2. 긴 텍스트를 입력창에 입력
  3. "요약하기" 버튼 클릭
  4. 하단에 요약된 결과 표시
  5. 최근 요약 내역 5개 표시

---

### 2. cardiffnlp/twitter-roberta-base-sentiment
- **태스크**: Sentiment Analysis (감정 분석)
- **설명**: 트위터 데이터로 학습된 RoBERTa 기반 감정 분석 모델로, 텍스트의 감정을 부정(Negative), 중립(Neutral), 긍정(Positive) 3가지로 분류합니다.
- **입력 예시 1**:
```
  I absolutely love this product! It exceeded all my expectations and works perfectly.
```
- **출력 예시 1**:
```
  감정: POSITIVE (긍정), 확률: 98.75%
```
- **입력 예시 2**:
```
  This is the worst experience I've ever had. Very disappointed.
```
- **출력 예시 2**:
```
  감정: NEGATIVE (부정), 확률: 99.12%
```
- **입력 예시 3**:
```
  The weather is okay today.
```
- **출력 예시 3**:
```
  감정: NEUTRAL (중립), 확률: 87.34%
```
- **실행 화면 예시**:
  1. 로그인 후 "감정 분석" 탭 클릭
  2. 분석할 영어 텍스트 입력
  3. "분석하기" 버튼 클릭
  4. 감정(긍정/중립/부정)과 확률 표시
  5. 최근 분석 내역 5개 표시

---

### 3. facebook/mbart-large-50-many-to-many-mmt
- **태스크**: Translation (번역)
- **설명**: Facebook에서 개발한 다국어 신경망 기계 번역 모델로, 50개 언어 간 번역을 지원합니다. 이 프로젝트에서는 영어를 한국어로 번역하는 데 사용됩니다.
- **모델 특징**:
  - 50개 언어 지원 (영어, 한국어, 일본어, 중국어, 프랑스어, 독일어 등)
  - Multilingual denoising pre-training 기반
  - 높은 번역 품질
- **입력 예시 1**:
```
  Hello, how are you today?
```
- **출력 예시 1**:
```
  안녕하세요, 오늘 어떻게 지내세요?
```
- **입력 예시 2**:
```
  Artificial intelligence is transforming the world.
```
- **출력 예시 2**:
```
  인공 지능이 세상을 변화시키고 있습니다.
```
- **입력 예시 3**:
```
  I love learning new technologies and programming languages.
```
- **출력 예시 3**:
```
  저는 새로운 기술과 프로그래밍 언어를 배우는 것을 좋아합니다.
```
- **입력 예시 4**:
```
  Machine learning models can process vast amounts of data efficiently.
```
- **출력 예시 4**:
```
  기계 학습 모델은 방대한 양의 데이터를 효율적으로 처리할 수 있습니다.
```
- **실행 화면 예시**:
  1. 로그인 후 "번역" 탭 클릭
  2. 번역할 영어 텍스트 입력
  3. "번역하기" 버튼 클릭
  4. 한국어 번역 결과 표시
  5. 최근 번역 내역 5개 표시

---

## 로그인 제한(Access Control)

### 공개 탭 (비로그인 허용)
- **요약(Summarize)** 탭은 로그인 없이 누구나 사용 가능
- 비로그인 상태에서는 세션에 임시 저장되며, 새로고침(F5) 시 초기화됨

### 제한 탭 (로그인 필요)
- **감정 분석(Sentiment)** 탭: 로그인 필요 🔒
- **번역(Translate)** 탭: 로그인 필요 🔒

### 접근 제한 동작
1. **비로그인 사용자가 제한 탭 클릭 시**:
   - "로그인 후 이용해주세요" alert 표시
   - 로그인 페이지로 자동 이동
   - 예시: `/accounts/login/?next=/sentiment`
   
2. **로그인 성공 후**:
   - 원래 가려던 페이지로 자동 복귀
   - 예: `/sentiment` 페이지로 접근하려다 로그인했다면, 로그인 후 자동으로 `/sentiment`로 이동

### 대화 내역 저장
- **로그인 유저**: 데이터베이스에 영구 저장 (최근 5개 표시, 전체 텍스트)
- **비로그인 유저**: 세션에 임시 저장 (새로고침 시 초기화, 최근 5개 표시)

---

## 설치 및 실행 방법

### 사전 요구사항
- Python 3.10 이상
- pip (Python 패키지 관리자)
- Git

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd Django_GPT
```

### 2. 가상환경 생성 및 활성화

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

> 💡 가상환경이 활성화되면 프롬프트 앞에 `(venv)`가 표시됩니다.

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

> ⚠️ **주의**: `huggingface-hub` 라이브러리가 필수입니다. Hugging Face API 엔드포인트 변경으로 인해 이 라이브러리를 사용합니다.

### 4. Hugging Face API 토큰 설정

#### 4-1. Hugging Face 토큰 발급
1. [Hugging Face](https://huggingface.co/) 가입 및 로그인
2. [토큰 생성 페이지](https://huggingface.co/settings/tokens) 접속
3. **"New token"** 클릭
4. **Token type: Read** 선택 ⚠️ (Fine-grained 아님!)
5. Name: 원하는 이름 입력 (예: `django-ai-project`)
6. **"Generate token"** 클릭
7. 생성된 토큰 복사 (예: `hf_xxxxxxxxxxxxxxxxxxxx`)

> ⚠️ **중요**: Token type을 **Read**로 선택해주세요!

#### 4-2. .env 파일 설정
프로젝트 루트 디렉토리(manage.py가 있는 위치)에 `.env` 파일을 생성하고 토큰을 입력하세요:
```env
HUGGINGFACE_API_TOKEN=hf_your_actual_token_here
```

**예시:**
```env
HUGGINGFACE_API_TOKEN=hf_abcdefghijklmnopqrstuvwxyz1234567890
```

> ⚠️ **중요**: 
> - `.env` 파일은 절대 GitHub에 업로드하지 마세요!
> - `.gitignore`에 `.env`가 포함되어 있는지 확인하세요.
> - 따옴표 없이, 공백 없이 입력하세요.

### 5. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 서버 실행
```bash
python manage.py runserver
```

서버가 정상적으로 실행되면 다음과 같은 메시지가 표시됩니다:
```
Django version 4.2.x, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 7. 브라우저에서 접속
```
http://127.0.0.1:8000/
```

또는
```
http://localhost:8000/
```

---

## 프로젝트 구조
```
Django_GPT/
├── manage.py                  # Django 관리 명령어
├── requirements.txt           # 필요한 패키지 목록
├── .env                       # API 토큰 (GitHub에 올리지 말 것!)
├── .gitignore                 # Git 제외 파일
├── README.md                  # 프로젝트 설명서
│
├── config/                    # 프로젝트 설정
│   ├── __init__.py
│   ├── settings.py            # Django 설정
│   ├── urls.py                # 메인 URL 라우팅
│   ├── wsgi.py
│   └── asgi.py
│
└── ai_app/                    # AI 기능 앱
    ├── __init__.py
    ├── models.py              # ChatHistory 모델
    ├── views.py               # 뷰 로직 (AI 모델 호출)
    ├── urls.py                # 앱 URL 패턴
    ├── admin.py               # 관리자 페이지
    ├── apps.py
    │
    ├── migrations/            # 데이터베이스 마이그레이션
    │   └── __init__.py
    │
    └── templates/             # HTML 템플릿
        ├── ai_app/
        │   ├── base.html      # 기본 레이아웃
        │   ├── home.html      # 홈페이지
        │   ├── summarize.html # 요약 페이지
        │   ├── sentiment.html # 감정 분석 페이지
        │   ├── translate.html # 번역 페이지
        │   └── signup.html    # 회원가입 페이지
        └── registration/
            └── login.html     # 로그인 페이지
```

---

## 주요 기능

### 1. 요약 (Summarize) - 공개 ✅
- **URL**: `/summarize`
- **로그인 불필요**: 누구나 사용 가능
- **모델**: facebook/bart-large-cnn
- **기능**: 긴 텍스트를 짧게 요약
- **대화 내역**: 
  - 로그인 시: DB 저장
  - 비로그인 시: 세션 저장 (새로고침 시 초기화)

### 2. 감정 분석 (Sentiment) - 로그인 필요 🔒
- **URL**: `/sentiment`
- **로그인 필수**: `@login_required` 데코레이터 적용
- **모델**: cardiffnlp/twitter-roberta-base-sentiment
- **기능**: 텍스트의 감정(긍정/중립/부정) 분석
- **대화 내역**: DB에 영구 저장

### 3. 번역 (Translate) - 로그인 필요 🔒
- **URL**: `/translate`
- **로그인 필수**: `@login_required` 데코레이터 적용
- **모델**: facebook/mbart-large-50-many-to-many-mmt
- **기능**: 영어를 한국어로 번역
- **대화 내역**: DB에 영구 저장

---

## 주의사항

### 보안 관련 ⚠️
- `.env` 파일은 절대 GitHub에 업로드하지 마세요!
- `SECRET_KEY`는 운영 환경에서 반드시 변경하세요
- 실제 운영 시 `DEBUG = False`로 설정하세요
- `ALLOWED_HOSTS`에 실제 도메인을 추가하세요

### API 사용 제한 ⚠️
- Hugging Face API는 무료 사용량 제한이 있습니다
- 첫 호출 시 모델 로딩으로 30초~1분 정도 소요될 수 있습니다
- "처리 중입니다..." 메시지가 표시되면 잠시 기다려주세요

### 네트워크 ⚠️
- 인터넷 연결이 필요합니다 (API 호출을 위해)
- 방화벽이나 프록시 설정을 확인하세요

---

## 문제 해결

### 1. ModuleNotFoundError: No module named 'dotenv'
**원인**: `python-dotenv` 패키지가 설치되지 않음

**해결**:
```bash
# 가상환경 활성화 확인
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 패키지 설치
pip install python-dotenv
```

### 2. ModuleNotFoundError: No module named 'huggingface_hub'
**원인**: `huggingface-hub` 패키지가 설치되지 않음

**해결**:
```bash
pip install huggingface-hub
```

### 3. API 토큰 오류
**원인**: `.env` 파일에 토큰이 올바르게 설정되지 않음

**해결**:
1. `.env` 파일이 프로젝트 루트(manage.py 위치)에 있는지 확인
2. 토큰 형식 확인: `HUGGINGFACE_API_TOKEN=hf_xxxxx` (따옴표 없이)
3. 토큰이 유효한지 [Hugging Face](https://huggingface.co/settings/tokens)에서 확인
4. 토큰이 **Read** 타입인지 확인
5. 서버 재시작: `python manage.py runserver`

### 4. 모델 호출 실패 오류
**원인**: 모델 로딩 중이거나 API 제한

**해결**:
- 첫 호출은 시간이 오래 걸립니다 (30초~1분)
- "처리 중입니다..." 메시지를 보고 기다려주세요
- 503 오류 발생 시 1-2분 후 다시 시도
- 토큰이 **Read** 타입으로 생성되었는지 확인

### 5. 데이터베이스 오류
**원인**: 마이그레이션이 실행되지 않음

**해결**:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 로그인 후 페이지 이동 안 됨
**원인**: `LOGIN_REDIRECT_URL` 설정 누락

**해결**:
- `config/settings.py`에 다음 추가:
```python
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

### 7. 번역 모델 401 에러
**원인**: 모델 접근 권한 문제

**해결**:
- 현재 사용 중인 `facebook/mbart-large-50-many-to-many-mmt` 모델은 공개 모델이므로 정상 작동합니다
- 토큰이 **Read** 타입인지 다시 확인하세요

### 8. 새로고침 시 히스토리가 안 사라짐 (비로그인)
**원인**: 세션 초기화 로직 누락

**확인**:
- `views.py`의 `summarize` 함수에서 GET 요청 시 세션 초기화 확인

---

## 참고 자료

### 사용 모델 문서
- [facebook/bart-large-cnn](https://huggingface.co/facebook/bart-large-cnn)
- [cardiffnlp/twitter-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)
- [facebook/mbart-large-50-many-to-many-mmt](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt)