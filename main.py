from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

# 우리가 만든 파일들 불러오기
from ai_model import SentimentAnalyzer
from database import engine, Base, get_db
import models

# --- 1. DB 테이블 자동 생성 ---
# 서버 켜질 때 models.py에 정의된 대로 테이블을 만듭니다.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- 2. 데이터 모델 (Pydantic) ---
class ReviewRequest(BaseModel):
    content: str

class ReviewResponse(BaseModel):
    id: int         # DB에 저장된 ID 추가
    content: str
    sentiment: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True # ORM 객체를 Pydantic 모델로 변환 허용

# --- 3. AI 모델 로딩 ---
print("서버 시작 중... AI 모델을 로드합니다.")
ai_analyzer = SentimentAnalyzer()
print("AI 모델 로드 완료!")

# --- 4. API 엔드포인트 ---
@app.post("/analyze", response_model=ReviewResponse)
def analyze_review(request: ReviewRequest, db: Session = Depends(get_db)):
    """
    1. 리뷰 내용 분석
    2. DB에 결과 저장
    3. 결과 반환
    """
    # [Step 1] AI 분석 수행
    result = ai_analyzer.analyze(request.content)
    
    # [Step 2] DB 저장용 객체(Model) 생성
    # models.Review 클래스의 인스턴스를 만듭니다.
    new_review = models.Review(
        content=result['text'],
        sentiment=result['sentiment'],
        confidence=float(result['confidence']) # 문자열을 숫자로 변환
    )
    
    # [Step 3] DB에 저장 (Transaction)
    db.add(new_review)  # 장바구니에 담기
    db.commit()         # 결제(저장) 확정
    db.refresh(new_review) # 저장된 정보(ID, 시간 등)를 다시 가져오기
    
    return new_review