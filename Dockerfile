# 1. 베이스 이미지 (Python 3.11이 설치된 리눅스 환경 가져오기)
# slim 버전을 쓰면 용량이 훨씬 가볍습니다.
FROM python:3.11-slim

# 2. 작업 디렉토리 설정 (리눅스 컴퓨터 안의 /app 폴더에서 작업하겠다)
WORKDIR /app

# 3. 필수 라이브러리 설치
# (캐시 효율을 위해 requirements.txt만 먼저 복사해서 설치)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 내 소스 코드 전체를 컨테이너 안으로 복사
COPY . .

# 5. 서버 실행 명령어 (uvicorn main:app ...)
# 0.0.0.0은 외부에서 접속 가능하게 열어두는 IP입니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]