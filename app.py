import streamlit as st
from google import genai
from PIL import Image

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手1", layout="centered")
st.title("🥛 牛奶比价记录助手1")

# 2. 初始化客户端
try:
    # 确保 Secrets 里的 key 名称一致
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("配置错误，请检查 Secrets")
    st.stop()

# 3. 上传与识别
uploaded_file = st.file_uploader("请上传图片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, width=300)
    if st.button("开始分析"):
        with st.spinner('正在分析...'):
            try:
                img = Image.open(uploaded_file)
                # 使用新版 SDK 的标准调用方式
                response = client.models.generate_content(
                    model='gemini-2.0-flash', # Google 新一代模型，默认权限最高
                    contents=[
                        "请提取图片中的单价和容量，计算折合250ml价格。格式：价格:X, 容量:Y, 折合250ml:Z。",
                        img
                    ]
                )
                st.write(response.text)
            except Exception as e:
                st.error(f"分析出错: {e}")
