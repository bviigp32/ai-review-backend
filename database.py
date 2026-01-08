from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DB 주소 설정 (지금은 sqlite 파일 사용)
# 나중에 PostgreSQL로 바꾸려면 이 줄만 바꾸면 됩니다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./reviews.db"

# 2. 엔진 생성 (DB와 연결되는 통로)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 세션 생성기 (DB에 작업 요청을 보낼 때마다 하나씩 생성)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델들의 조상 클래스 (이걸 상속받아야 테이블이 됨)
Base = declarative_base()

# 5. DB 세션을 가져오는 함수 (FastAPI에서 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()