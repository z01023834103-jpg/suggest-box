import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="한 줄 건의함", page_icon="📮", layout="centered")

# 세션 상태(저장소) 초기화
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

st.title("📮 익명 한 줄 건의함")
st.caption("자유롭게 한 줄로 의견을 남겨주세요. (익명 보장)")

# 입력 폼 생성 (clear_on_submit=True로 제출 시 입력창 자동 비움)
with st.form(key="suggestion_form", clear_on_submit=True):
    user_input = st.text_input(
        label="건의 내용을 입력하세요",
        placeholder="예: 휴게실 의자를 바꿔주세요!",
        max_chars=100
    )
    submit_button = st.form_submit_button(label="제출하기", use_container_width=True)

# 제출 로직 처리
if submit_button:
    # 공백 제거 후 빈 내용 검사
    cleaned_input = user_input.strip()
    if cleaned_input:
        # 최신 건의가 맨 앞에 오도록 0번 인덱스에 추가
        st.session_state.suggestions.insert(0, cleaned_input)
        st.success("건의가 성공적으로 등록되었습니다.")
    else:
        st.warning("내용을 입력해 주세요.")

st.divider()

# 등록된 건의사항 목록 출력 (최신순)
st.subheader("📋 등록된 건의 목록")

if st.session_state.suggestions:
    for idx, item in enumerate(st.session_state.suggestions):
        st.info(f"• {item}")
else:
    st.text_container()
    st.write("아직 등록된 건의가 없습니다. 첫 번째 건의를 남겨보세요!")