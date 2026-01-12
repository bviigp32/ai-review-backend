import logging
from fastapi import FastAPI
from database import engine
import models

# 우리가 만든 라우터 불러오기
from routers import reviews, analytics

# 1. 로깅 설정 (서버 기록 남기기)
# INFO 레벨 이상의 로그를 출력하고, 날짜와 시간을 포함시킴
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 2. DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Review Analyzer", version="1.0.0")

# 3. 라우터 등록 (이게 핵심!)
app.include_router(reviews.router)
app.include_router(analytics.router)

@app.on_event("startup")
async def startup_event():
    logger.info("서버가 성공적으로 시작되었습니다!")

@app.get("/")
def read_root():
    logger.info("메인 페이지 접속 요청 발생")
    return {"message": "Welcome to AI Review Analyzer API"}