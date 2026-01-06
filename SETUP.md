# 프로젝트 설정 가이드

## 초기 설정 (처음 한 번만)

### 1. Python 가상환경 설정
```bash
# 소스 폴더로 이동
cd src

python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
`.env` 파일을 프로젝트 루트에 생성하고 다음 내용을 추가:
```
SECRET_KEY=your-secret-key-here
SECRET_PASSWORD=your-secret-password-here
```

### 4. 데이터베이스 마이그레이션
```bash
python manage.py migrate
```

### 5. Tailwind CSS 설정

**SSL 인증서 문제 해결:**
```bash
# certifi 업그레이드
pip install --upgrade certifi

# Tailwind CSS 빌드 (SSL 검증 포함)
SSL_CERT_FILE=$(python -m certifi) python manage.py tailwind build
```

**또는 자동 스크립트 사용:**
```bash
chmod +x setup_tailwind.sh
./setup_tailwind.sh
```

## 개발 서버 실행

### 기본 실행 (가장 간단)
```bash
python manage.py runserver
```

이미 빌드된 CSS 파일(`theme/static/css/dist/styles.css`)이 있으므로 대부분의 경우 이것만으로 충분합니다.

### Tailwind 스타일 수정 시
스타일을 변경하는 경우에만 Tailwind watch 모드가 필요합니다:

**터미널 1:**
```bash
SSL_CERT_FILE=$(python -m certifi) python manage.py tailwind start
```

**터미널 2:**
```bash
python manage.py runserver
```

## SSL 인증서 에러가 계속 발생하는 경우

### macOS
1. Python 인증서 설치 스크립트 실행:
```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

2. 또는 수동으로 certifi 설치:
```bash
pip install --upgrade certifi
export SSL_CERT_FILE=$(python -m certifi)
```

### 임시 해결책 (권장하지 않음)
개발 환경에서만 사용:
```bash
export PYTHONHTTPSVERIFY=0
python manage.py tailwind build
```

## 사용자 역할

### 일반 사용자
- 회원가입 시 전화번호로 가입
- 로그인 후 질문 작성/조회 가능
- Superadmin 승인 필요 (`permission=True`)

### 운영진 (Executive)
- 회원가입 시 'Executive' 선택
- 비밀번호 설정 필요
- 로그인 후 운영진 대시보드 접근
- 미답변 질문 관리, 카테고리 관리

### Superadmin
- `.env`의 `SECRET_KEY`와 `SECRET_PASSWORD`로 로그인
- 모든 사용자 승인 권한

## 프로젝트 구조

```
hackathon_pirostack/
├── hackathon/          # 프로젝트 설정
├── users/              # 사용자 인증
├── questions/          # 질문/답변 앱
├── discussions/        # 토론 앱
├── theme/              # Tailwind CSS
│   └── static/css/dist/styles.css  # 빌드된 CSS (이미 커밋됨)
└── requirements.txt
```

## 문제 해결

### Tailwind가 적용되지 않는 경우
1. `theme/static/css/dist/styles.css` 파일이 있는지 확인
2. 없다면: `./setup_tailwind.sh` 실행
3. 브라우저 캐시 삭제 (Cmd+Shift+R)

### "Page not found" 에러
- URL 확인: `/login/` 또는 `/users/`로 접속

### 운영진 페이지 접근 불가
- 회원가입 시 'Executive' 선택했는지 확인
- 비밀번호 설정했는지 확인
- 로그인 후 자동으로 `/questions/staff/`로 이동

## 배포 전 체크리스트

- [ ] `python manage.py tailwind build` 실행
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] `DEBUG=False` 설정
- [ ] `ALLOWED_HOSTS` 설정
- [ ] 정적 파일 수집: `python manage.py collectstatic`
