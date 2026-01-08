import pandas as pd

# 데이터 경로 (탭으로 구분되어 있으므로 sep='\t', 헤더가 없으므로 header=None)
# 컬럼 이름은 임의로 rating, review로 지정
df = pd.read_csv('data/naver_shopping.txt', sep='\t', header=None, names=['rating', 'review'])

print("=== 데이터 상위 5개 ===")
print(df.head())

print("\n=== 데이터 정보 ===")
print(df.info())

# 저장 테스트 (CSV로 변환해서 저장해보기)
df.to_csv('data/shopping_reviews.csv', index=False)
print("\nCSV 변환 저장 완료!")