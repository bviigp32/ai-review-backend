from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, desc # func: 집계함수(COUNT, AVG 등), desc: 내림차순 정렬

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

# 통계 정보를 보여줄 스키마
class StatsResponse(BaseModel):
    total_count: int
    positive_count: int
    negative_count: int
    positive_ratio: float  # 긍정 비율 (%)
    average_confidence: float # AI가 얼마나 확신하는지 평균

# 랭킹 정보를 보여줄 스키마 (리스트 형태)
class RankingResponse(BaseModel):
    best_reviews: list[ReviewResponse] # 우리가 이전에 만든 ReviewResponse 재활용
    worst_reviews: list[ReviewResponse]

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

# --- 5. 통계/분석 API ---

@app.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """
    [데이터 분석] 전체 리뷰 통계 정보를 반환합니다.
    """
    # 1. 전체 개수
    total_count = db.query(func.count(models.Review.id)).scalar()
    
    # 2. 긍정/부정 개수
    pos_count = db.query(func.count(models.Review.id)).filter(models.Review.sentiment == '긍정').scalar()
    neg_count = db.query(func.count(models.Review.id)).filter(models.Review.sentiment == '부정').scalar()
    
    # 3. 평균 확신도 (AI가 얼마나 똑똑하게 판단했는지)
    avg_conf = db.query(func.avg(models.Review.confidence)).scalar()
    
    # 예외 처리 (데이터가 0개일 경우 0으로 나누기 방지)
    if total_count == 0:
        return StatsResponse(
            total_count=0, positive_count=0, negative_count=0, 
            positive_ratio=0.0, average_confidence=0.0
        )
    
    return StatsResponse(
        total_count=total_count,
        positive_count=pos_count,
        negative_count=neg_count,
        positive_ratio=(pos_count / total_count) * 100, # 백분율 계산
        average_confidence=avg_conf if avg_conf else 0.0
    )

@app.get("/ranking", response_model=RankingResponse)
def get_ranking(db: Session = Depends(get_db)):
    """
    [데이터 분석] 가장 긍정적인 리뷰와 가장 부정적인 리뷰 Top 3를 뽑습니다.
    """
    # 1. 가장 긍정적인 리뷰 (긍정적이면서 확신도가 높은 순)
    best_reviews = db.query(models.Review)\
        .filter(models.Review.sentiment == '긍정')\
        .order_by(desc(models.Review.confidence))\
        .limit(3).all()
        
    # 2. 가장 부정적인 리뷰 (부정적이면서 확신도가 높은 순)
    worst_reviews = db.query(models.Review)\
        .filter(models.Review.sentiment == '부정')\
        .order_by(desc(models.Review.confidence))\
        .limit(3).all()
        
    return RankingResponse(best_reviews=best_reviews, worst_reviews=worst_reviews)