import os
import streamlit as st
from supabase import create_client, Client

# 페이지 기본 설정
st.set_page_config(page_title="한 줄 건의함", page_icon="📮", layout="centered")

# 환경 변수에서 Supabase 설정 불러오기
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# (선택) Streamlit Cloud 환경 등에서 st.secrets를 대비한 예외 처리
if not SUPABASE_URL or not SUPABASE_KEY:
    try:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ SUPABASE_URL 또는 SUPABASE_KEY 환경 변수가 설정되지 않았습니다.")
    st.stop()

# Supabase 클라이언트 초기화 (캐싱 적용)
@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

st.title("📮 Supabase 익명 한 줄 건의함")
st.caption("자유롭게 의견을 남겨주세요. (실시간 데이터베이스 연동)")

# 입력 폼 생성 (content와 category 반영)
with st.form(key="suggestion_form", clear_on_submit=True):
    category = st.selectbox(
        label="카테고리",
        options=["시설/환경", "학업/수업", "행사/활동", "기타"]
    )
    user_input = st.text_input(
        label="건의 내용을 입력하세요",
        placeholder="예: 휴게실 의자를 바꿔주세요!",
        max_chars=100
    )
    submit_button = st.form_submit_button(label="제출하기", use_container_width=True)

# 제출 로직 처리
if submit_button:
    cleaned_input = user_input.strip()
    if cleaned_input:
        try:
            # Supabase suggestions 테이블에 데이터 삽입
            data = {
                "content": cleaned_input,
                "category": category,
                "likes": 0
            }
            response = supabase.table("suggestions").insert(data).execute()
            st.success("건의가 성공적으로 등록되었습니다.")
            st.rerun()  # 최신 목록 반영을 위해 앱 재실행
        except Exception as e:
            st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
    else:
        st.warning("내용을 입력해 주세요.")

st.divider()

# 등록된 건의사항 목록 출력 (created_at 기준 최신순 정렬)
st.subheader("📋 등록된 건의 목록")

try:
    response = supabase.table("suggestions").select("*").order("created_at", desc=True).execute()
    suggestions = response.data
    
    if suggestions:
        for item in suggestions:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.info(f"**[{item.get('category', '기타')}]** {item.get('content')}")
            with col2:
                # 좋아요 기능 버튼
                if st.button("❤️", key=f"like_{item.get('id')}"):
                    new_likes = (item.get('likes') or 0) + 1
                    supabase.table("suggestions").update({"likes": new_likes}).eq("id", item.get('id')).execute()
                    st.rerun()
            
            # 등록일 및 좋아요 수 표시
            created_date = item.get('created_at', '')[:10] if item.get('created_at') else ''
            st.caption(f"등록일: {created_date} | 좋아요: {item.get('likes', 0)}개")
    else:
        st.write("아직 등록된 건의가 없습니다. 첫 번째 건의를 남겨보세요!")
        
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")