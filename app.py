import streamlit as st
import datetime
import google.generativeai as genai

# 1. 우리만의 기념일 세팅 (2025년 9월 12일 시작)
ANNIVERSARY = datetime.date(2025, 9, 12) 
PRIVATE_PASSWORD = "1234" # 우리만의 비밀번호 (원하는 대로 바꾸세요!)

st.set_page_config(page_title="우리만의 공간", page_icon="💖")

# 비밀번호 확인 로직
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("🔒 우리 비밀번호가 뭐더라?")
    pwd = st.text_input("비밀번호 입력", type="password")
    if st.button("들어가기"):
        if pwd == PRIVATE_PASSWORD:
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("틀렸어! 다시 생각해봐.")
    st.stop()

# 메인 화면
today = datetime.date.today()
d_day = (today - ANNIVERSARY).days + 1

st.title("💖 우리 사귄 지 벌써..")
st.header(f"{d_day}일째!")
st.write(f"처음 만난 날: {ANNIVERSARY}")

st.divider()
st.subheader("💌 Gemini에게 일기 보여주기")
diary = st.text_area("오늘 무슨 일이 있었어?")
api_key = "여기에_진짜_API_KEY를_넣으세요" # 구글 AI 스튜디오에서 받은 키!

if st.button("AI 분석 시작"):
    if diary and api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"커플 상담사로서 이 일기에 다정하게 답장해줘: {diary}")
            st.info(res.text)
        except Exception as e:
            st.error(f"에러가 발생했어요: {e}")
