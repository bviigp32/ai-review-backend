# AI Shopping Review Analyzer (AI 쇼핑 리뷰 분석기)

사용자의 쇼핑 리뷰 텍스트를 입력받아 **AI(Deep Learning)** 모델을 통해 긍정/부정을 분석하고, 통계 데이터를 제공하는 백엔드 API 서비스입니다.

## 프로젝트 소개
이 프로젝트는 대량의 리뷰 데이터를 효율적으로 처리하고, 비즈니스 인사이트를 도출하기 위해 구축되었습니다.
단순한 CRUD를 넘어 **AI 모델 서빙**, **대용량 데이터 배치 처리**, **데이터 분석 API**까지 포함된 올인원 백엔드 파이프라인을 지향합니다.

## 기술 스택 (Tech Stack)
- **Language**: Python 3.11
- **Framework**: FastAPI
- **Visualization**: Streamlit, Plotly  
- **AI/ML**: Hugging Face Transformers (KoELECTRA Model), PyTorch
- **Database**: SQLite (SQLAlchemy ORM)
- **Data Engineering**: Pandas, TQDM (Batch Processing)

## 주요 기능 (Key Features)
1.  **AI 감정 분석 (Sentiment Analysis)**
    - 한국어 리뷰 텍스트를 분석하여 긍정/부정 판단 및 확신도(Confidence) 출력
    - Hugging Face의 Pre-trained 모델 서빙 최적화 (Singleton Pattern 적용)
2.  **대용량 데이터 배치 처리 (Batch Processing)**
    - 20만 건 이상의 리뷰 데이터를 배치 단위로 DB에 고속 적재 (Bulk Insert)
3.  **실시간 통계 및 랭킹 분석**
    - 전체 리뷰의 긍정/부정 비율 자동 계산 (`/stats`)
    - 확신도가 높은 'Best 리뷰'와 'Worst 리뷰' Top 3 추출 (`/ranking`)
4. **데이터 시각화 대시보드 (Interactive Dashboard)** 
    - Streamlit 기반의 웹 대시보드 제공
    - 긍정/부정 비율 파이 차트 및 리뷰 랭킹 테이블 시각화

## API 명세 (API Usage)

### 1. 리뷰 분석 요청
**POST** `/analyze`
```json
{
  "content": "배송도 빠르고 상품 퀄리티가 너무 좋아요!"
}
```

### 2. 통계 조회
**GET** `/stats`
- 전체 리뷰 수, 긍정/부정 비율, 평균 확신도 반환

### 3. 랭킹 조회
**GET** `/ranking`
- 가장 긍정적인/부정적인 리뷰 Top 3 반환

## 실행 방법 (How to Run)

### 1. Backend Server 실행
```bash
uvicorn main:app --reload
```
API 서버는 http://127.0.0.1:8000에서 실행됩니다.

2. Dashboard 실행

```bash
streamlit run dashboard.py
```
대시보드는 http://localhost:8501에서 자동으로 열립니다.

---
Dev Log: 매일 기능을 추가하며 업데이트 중입니다.


