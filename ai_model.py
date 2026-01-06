from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        print("AI 모델을 로딩하고 있습니다... (최초 실행 시 시간이 걸립니다)")
        # Hugging Face에서 한국어 감정 분석 모델을 다운로드 및 로드합니다.
        # model: 사용할 모델 ID, task: 수행할 작업(감정 분석)
        self.classifier = pipeline(
            "sentiment-analysis",
            model="matthewburke/korean_sentiment"
        )
        print("AI 모델 로딩 완료!")

    def analyze(self, text: str):
        """
        문자열을 받아 긍정/부정 결과와 확률을 반환합니다.
        """
        # 모델 예측 실행 (최대 512자까지만 처리하도록 설정)
        result = self.classifier(text[:512])[0]
        
        # result 형태: {'label': 'LABEL_1', 'score': 0.98...}
        # LABEL_1: 긍정, LABEL_0: 부정 (모델마다 다를 수 있으니 확인 필요)
        
        label = result['label']
        score = result['score']

        # 사람이 보기 좋게 변환
        if label == 'LABEL_1':
            sentiment = "긍정"
        else:
            sentiment = "부정"
        
        return {
            "text": text,
            "sentiment": sentiment,
            "confidence": f"{score:.2f}", # 소수점 2자리까지
            "raw_label": label
        }

# --- 테스트 코드 (이 파일만 실행했을 때 동작) ---
if __name__ == "__main__":
    # 클래스 인스턴스 생성
    ai = SentimentAnalyzer()

    # 테스트 문장들
    test_sentences = [
        "배송도 빠르고 상품도 아주 마음에 듭니다!",
        "진짜 최악이에요. 다신 안 삽니다.",
        "그냥 보통이에요. 쓸만합니다.",
        "생각보다 별로네요. 환불하고 싶어요."
    ]

    print("\n--- 분석 결과 테스트 ---")
    for sent in test_sentences:
        res = ai.analyze(sent)
        print(f"문장: {res['text']}")
        print(f"결과: {res['sentiment']} (확률: {res['confidence']})")
        print("-" * 30)