import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="牛奶比价助手22")
st.title("🥛 牛奶比价助手")

# 直接配置 API Key
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 使用 gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("请上传图片", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("开始识别"):
    try:
        img = Image.open(uploaded_file)
        response = model.generate_content(["识别价格容量，计算折合250ml价格", img])
        st.write(response.text)
    except Exception as e:
        st.error(f"出错: {e}")
