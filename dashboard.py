import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os  

# 1. 페이지 기본 설정 (제목, 레이아웃)
st.set_page_config(page_title="Review Dashboard", layout="wide")

st.title("AI Review Analytics Dashboard")
st.markdown("---")

# [수정 후] 환경변수에서 주소를 가져오고, 없으면 기본값(127.0.0.1) 사용
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# 2. 데이터 가져오기 함수
def fetch_stats():
    try:
        response = requests.get(f"{API_URL}/analytics/stats")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("데이터를 가져오는데 실패했습니다.")
            return None
    except:
        st.error("백엔드 서버가 켜져있는지 확인해주세요!")
        return None

def fetch_ranking():
    try:
        response = requests.get(f"{API_URL}/analytics/ranking")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# 3. 메인 화면 구성
stats = fetch_stats()
ranking = fetch_ranking()

if stats:
    # [Section 1] 핵심 지표 (Metric) 보여주기
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("총 리뷰 수", f"{stats['total_count']}건")
    col2.metric("긍정 리뷰", f"{stats['positive_count']}건")
    col3.metric("부정 리뷰", f"{stats['negative_count']}건")
    col4.metric("평균 AI 확신도", f"{stats['average_confidence'] * 100:.1f}%")

    st.markdown("---")

    # [Section 2] 차트 그리기 (긍정/부정 비율)
    st.subheader("긍정 vs 부정 비율")
    
    # 데이터프레임 만들기
    df_sentiment = pd.DataFrame({
        "감정": ["긍정", "부정"],
        "개수": [stats['positive_count'], stats['negative_count']]
    })
    
    # Plotly로 파이 차트 그리기
    fig = px.pie(df_sentiment, values='개수', names='감정', 
                 title='리뷰 감정 분포', 
                 color='감정',
                 color_discrete_map={'긍정':'blue', '부정':'red'})
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # [Section 3] 랭킹 보여주기 (Top 3)
    if ranking:
        col_best, col_worst = st.columns(2)
        
        with col_best:
            st.success("🏆 Best Reviews (긍정 Top 3)")
            # 보기 좋게 데이터프레임으로 변환
            df_best = pd.DataFrame(ranking['best_reviews'])
            if not df_best.empty:
                st.dataframe(df_best[['content', 'confidence']], hide_index=True)

        with col_worst:
            st.error("Worst Reviews (부정 Top 3)")
            df_worst = pd.DataFrame(ranking['worst_reviews'])
            if not df_worst.empty:
                st.dataframe(df_worst[['content', 'confidence']], hide_index=True)

else:
    st.warning("데이터가 없습니다. 먼저 백엔드 서버를 실행하고 데이터를 쌓아주세요.")

# 사이드바 (새로고침 버튼)
if st.sidebar.button("데이터 새로고침"):
    st.rerun()