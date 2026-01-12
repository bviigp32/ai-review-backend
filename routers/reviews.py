from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

# 상위 폴더의 모듈을 가져오기 위한 설정
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import get_db
import models
from ai_model import SentimentAnalyzer

# 라우터 설정 (Prefix: 이 파일의 모든 API는 앞에 /reviews가 붙음)
router = APIRouter(prefix="/reviews", tags=["Reviews"])

# AI 모델은 여기서 로딩 (또는 main에서 주입받을 수도 있지만, 일단 독립적으로 둠)
# 주의: 실제 운영에선 main.py에서 로딩해서 넘겨주는 게 더 좋지만, 
# 코드 복잡도를 줄이기 위해 여기서 호출합니다. (Singleton 효과는 유지됨)
ai_analyzer = SentimentAnalyzer()

# --- Pydantic 모델  ---
class ReviewRequest(BaseModel):
    content: str

class ReviewResponse(BaseModel):
    id: int
    content: str
    sentiment: str
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- API 엔드포인트 ---
@router.post("/analyze", response_model=ReviewResponse)
def analyze_review(request: ReviewRequest, db: Session = Depends(get_db)):
    """
    [리뷰 분석] 텍스트를 분석하고 DB에 저장합니다.
    URL: POST /reviews/analyze
    """
    # 1. AI 분석
    result = ai_analyzer.analyze(request.content)
    
    # 2. DB 저장
    new_review = models.Review(
        content=result['text'],
        sentiment=result['sentiment'],
        confidence=float(result['confidence'])
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return new_review