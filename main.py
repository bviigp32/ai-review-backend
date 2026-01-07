from fastapi import FastAPI
from pydantic import BaseModel
from ai_model import SentimentAnalyzer # 어제 만든 AI 클래스 불러오기

app = FastAPI()

# --- 1. 데이터 모델 정의 (Pydantic) ---
# 요청(Request) 받을 데이터 형태: 사용자가 보낼 JSON 구조
class ReviewRequest(BaseModel):
    content: str  # 리뷰 내용 (필수)

# 응답(Response) 줄 데이터 형태: 서버가 돌려줄 JSON 구조
class ReviewResponse(BaseModel):
    text: str
    sentiment: str
    confidence: str

# --- 2. AI 모델 로딩 (서버 시작 시 1회 실행) ---
# 전역 변수로 인스턴스를 생성하면 서버가 켜질 때 모델을 다운/로드합니다.
# 요청이 들어올 때마다 로딩하는 것을 방지하여 속도를 높입니다.
print("서버 시작 중... AI 모델을 로드합니다.")
ai_analyzer = SentimentAnalyzer()
print("AI 모델 로드 완료! 서버 준비 끝.")

# --- 3. API 엔드포인트 정의 ---
@app.get("/")
def read_root():
    return {"message": "AI Review Analyzer Server is Running!"}

@app.post("/analyze", response_model=ReviewResponse)
def analyze_review(request: ReviewRequest):
    """
    리뷰 내용을 받아서 감정을 분석하고 결과를 반환합니다.
    """
    # 1. 사용자가 보낸 내용 꺼내기
    review_text = request.content
    
    # 2. AI 모델에게 분석 시키기
    result = ai_analyzer.analyze(review_text)
    
    # 3. 결과 반환 (Pydantic 모델에 맞춰서)
    return ReviewResponse(
        text=result['text'],
        sentiment=result['sentiment'],
        confidence=result['confidence']
    )