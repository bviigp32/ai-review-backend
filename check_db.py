from database import SessionLocal
from models import Review

db = SessionLocal()
count = db.query(Review).count()
reviews = db.query(Review).limit(5).all()

print(f"📊 현재 DB에 저장된 총 데이터 개수: {count}개")
print("\n--- 최신 데이터 5개 ---")
for r in reviews:
    print(f"[{r.sentiment}] {r.content[:30]}... ({r.confidence})")

db.close()