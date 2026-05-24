import streamlit as st
import datetime
import google.generativeai as genai
from PIL import Image

# 1. 우리만의 기념일 세팅 (2025년 9월 12일 시작)
ANNIVERSARY = datetime.date(2025, 9, 12) 
PRIVATE_PASSWORD = "3829" # 우리만의 비밀번호 (원하는 대로 바꾸세요!)

st.set_page_config(page_title="우리만의 공간", page_icon="💖", layout="centered")

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

# ✨ 새로 추가된 기능: 우리만의 사진 앨범 섹션
st.subheader("📸 우리들의 순간 기록 (사진 업로드)")
st.write("오늘 데이트한 사진이나 같이 보고 싶은 사진을 올려보세요!")

# 이미지 업로드 컴포넌트
uploaded_file = st.file_uploader("여기에 사진 파일을 올려주세요 (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 이미지를 열어서 화면에 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 방금 올린 우리 사진", use_container_width=True)
    
    # 사진에 대한 간단한 한 줄 메모 기능
    photo_memo = st.text_input("이 사진에 소중한 한 줄 메모를 남겨보세요", placeholder="예: 오늘 삼겹살 맛집에서 한 컷! 너무 맛있었다..")
    if photo_memo:
        st.success(f"📝 메모 저장 완료: {photo_memo}")

st.divider()

# 3. Google AI Studio (Gemini) 일기장 공간
st.subheader("💌 Gemini에게 일기 보여주기")
diary = st.text_area("오늘 무슨 일이 있었어?")
api_key = "AIzaSyDYHWL72TiASDf2bSyXa63RyPVThZ55xnI" # 🚨 유저님의 진짜 구글 API Key를 여기에 다시 입력하세요!

if st.button("AI 분석 시작"):
    if diary and api_key and api_key != "AIzaSyDYHWL72TiASDf2bSyXa63RyPVThZ55xnI":
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"커플 상담사로서 이 일기에 다정하게 답장해줘: {diary}")
            st.info(res.text)
        except Exception as e:
            st.error(f"에러가 발생했어요: {e}")
    else:
        st.warning("일기를 작성하거나 API Key가 정확히 입력되었는지 확인해주세요!")
