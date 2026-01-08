from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Review(Base):
    __tablename__ = "reviews" # 실제 DB에 저장될 테이블 이름

    id = Column(Integer, primary_key=True, index=True)  # 고유 번호
    content = Column(String, index=True)                # 리뷰 내용
    sentiment = Column(String)                          # 긍정/부정 결과
    confidence = Column(Float)                          # 확신 확률 (0.99 등)
    created_at = Column(DateTime, default=datetime.now) # 저장된 시간