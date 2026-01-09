import pandas as pd
from tqdm import tqdm # 진행바 표시
from sqlalchemy.orm import Session

# 우리가 만든 모듈들
from database import SessionLocal, engine
import models
from ai_model import SentimentAnalyzer

def process_data(limit=100):
    """
    데이터 파일에서 리뷰를 읽어와 AI 분석 후 DB에 저장합니다.
    limit: 처리할 데이터 개수 (None이면 전체 처리)
    """
    
    # 1. DB 세션 생성
    db = SessionLocal()
    
    # 2. AI 모델 로딩 (시간이 좀 걸림)
    print("🤖 AI 모델을 로딩 중입니다...")
    ai = SentimentAnalyzer()
    
    # 3. 데이터 파일 읽기 (Pandas 활용)
    print("📂 데이터 파일을 읽는 중입니다...")
    # 헤더가 없으므로 names로 컬럼명 지정
    df = pd.read_csv('data/naver_shopping.txt', sep='\t', header=None, names=['rating', 'review'])
    
    # 데이터가 너무 많으니 테스트용으로 일부만 자르기
    if limit:
        df = df.head(limit)
        print(f"⚠️ 테스트를 위해 상위 {limit}개만 처리합니다.")
    
    print(f"🚀 총 {len(df)}개의 리뷰 분석을 시작합니다!")

    # 4. 반복문으로 분석 및 저장 (tqdm으로 진행바 표시)
    buffer = [] # 데이터를 모아둘 리스트
    batch_size = 10 # 10개씩 모아서 DB에 저장 (속도 향상)

    for index, row in tqdm(df.iterrows(), total=len(df)):
        review_text = row['review']
        
        try:
            # (1) AI 분석
            result = ai.analyze(review_text)
            
            # (2) DB 모델 객체 생성
            new_review = models.Review(
                content=result['text'],
                sentiment=result['sentiment'],
                confidence=float(result['confidence'])
            )
            
            buffer.append(new_review)
            
            # (3) 배치가 꽉 차면 DB에 저장 (Bulk Insert 효과)
            if len(buffer) >= batch_size:
                db.add_all(buffer) # 한 번에 추가
                db.commit()        # 저장 확정
                buffer = []        # 버퍼 비우기
                
        except Exception as e:
            print(f"\n❌ 에러 발생 (Index {index}): {e}")
            continue

    # 남은 데이터가 있다면 마저 저장
    if buffer:
        db.add_all(buffer)
        db.commit()

    print("\n✅ 모든 작업이 완료되었습니다!")
    db.close()

if __name__ == "__main__":
    # 여기서 처리할 개수를 조절하세요. (예: 100, 1000, 5000...)
    # None으로 하면 20만 개 전체를 돌립니다.
    process_data(limit=100)