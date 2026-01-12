from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import List

# 상위 모듈 import
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import get_db
import models
# ReviewResponse는 reviews.py에 있는걸 쓰거나, 여기서 재정의해야 함.
# 편의상 여기서 필요한 모델만 간단히 재정의 
from routers.reviews import ReviewResponse 

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# --- Pydantic 스키마 ---
class StatsResponse(BaseModel):
    total_count: int
    positive_count: int
    negative_count: int
    positive_ratio: float
    average_confidence: float

class RankingResponse(BaseModel):
    best_reviews: List[ReviewResponse]
    worst_reviews: List[ReviewResponse]

# --- API 엔드포인트 ---
@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_count = db.query(func.count(models.Review.id)).scalar()
    
    if total_count == 0:
        return StatsResponse(
            total_count=0, positive_count=0, negative_count=0, 
            positive_ratio=0.0, average_confidence=0.0
        )

    pos_count = db.query(func.count(models.Review.id)).filter(models.Review.sentiment == '긍정').scalar()
    neg_count = db.query(func.count(models.Review.id)).filter(models.Review.sentiment == '부정').scalar()
    avg_conf = db.query(func.avg(models.Review.confidence)).scalar()
    
    return StatsResponse(
        total_count=total_count,
        positive_count=pos_count,
        negative_count=neg_count,
        positive_ratio=(pos_count / total_count) * 100,
        average_confidence=avg_conf if avg_conf else 0.0
    )

@router.get("/ranking", response_model=RankingResponse)
def get_ranking(db: Session = Depends(get_db)):
    best_reviews = db.query(models.Review).filter(models.Review.sentiment == '긍정')\
        .order_by(desc(models.Review.confidence)).limit(3).all()
        
    worst_reviews = db.query(models.Review).filter(models.Review.sentiment == '부정')\
        .order_by(desc(models.Review.confidence)).limit(3).all()
        
    return RankingResponse(best_reviews=best_reviews, worst_reviews=worst_reviews)