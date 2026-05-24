import streamlit as st
import datetime
import google.generativeai as genai
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore, storage
import io

# 1. Firebase 초기화 (깃허브에 올린 json 열쇠 사용)
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase_key.json')
    # Firebase 콘솔 Storage 탭 상단에 있는 gs://로 시작하는 주소를 아래에 적어주세요.
    # 예: 'your-project-id.appspot.com' (gs://는 제외)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'firstweek12n-design.appspot.com'  # 🚨 유저님의 Firebase Storage 버킷 주소로 자동 매핑을 시도합니다. 안 맞으면 수정 필요!
    })

db = firestore.client()
bucket = storage.bucket()

# 2. 우리만의 기념일 세팅
ANNIVERSARY = datetime.date(2025, 9, 12) 
PRIVATE_PASSWORD = "1234"

st.set_page_config(page_title="우리만의 공간", page_icon="💖", layout="centered")

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

# 메인 디데이 화면
today = datetime.date.today()
d_day = (today - ANNIVERSARY).days + 1
st.title("💖 우리 사귄 지 벌써..")
st.header(f"{d_day}일째!")

st.divider()

# 📸 사진 업로드 및 Firebase 저장 섹션
st.subheader("📸 우리들의 순간 기록 (Firebase 영구 저장)")
uploaded_file = st.file_uploader("사진을 올리면 데이터베이스에 저장됩니다", type=["png", "jpg", "jpeg"])
photo_memo = st.text_input("사진 한 줄 메모")

if st.button("추억 저장소에 업로드하기") and uploaded_file is not None:
    with st.spinner("Firebase에 추억을 저장하는 중..."):
        # 1. Storage에 이미지 파일 업로드
        file_bytes = uploaded_file.read()
        blob = bucket.blob(f"photos/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}")
        blob.upload_from_string(file_bytes, content_type=uploaded_file.type)
        blob.make_public()
        img_url = blob.public_url
        
        # 2. Firestore 데이터베이스에 기록 저장
        doc_ref = db.collection("gallery").document()
        doc_ref.set({
            "img_url": img_url,
            "memo": photo_memo,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success("🎉 Firebase에 안전하게 저장되었습니다! 새로고침해도 안 날아가요!")
        st.rerun()

# 🖼️ Firebase에서 저장된 추억들 다시 불러와서 화면에 뿌려주기
st.write("### 📜 우리들의 누적 앨범")
docs = db.collection("gallery").order_by("date", direction=firestore.Query.DESCENDING).stream()
for doc in docs:
    data = doc.to_dict()
    st.image(data["img_url"], use_container_width=True)
    if data["memo"]:
        st.info(f"📅 {data['date']} | {data['memo']}")
    st.write("---")

st.divider()

# 3. Gemini 일기장 공간
st.subheader("💌 Gemini에게 일기 보여주기")
diary = st.text_area("오늘 무슨 일이 있었어?")
api_key = "여기에_진짜_API_KEY를_넣으세요" # 🚨 유저님의 진짜 구글 API Key 입력!

if st.button("AI 분석 시작"):
    if diary and api_key and api_key != "여기에_진짜_API_KEY를_넣으세요":
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"커플 상담사로서 이 일기에 다정하게 답장해줘: {diary}")
            st.info(res.text)
        except Exception as e:
            st.error(f"에러가 발생했어요: {e}")
