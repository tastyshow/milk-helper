import streamlit as st
from google import genai
import pandas as pd

# 1. 页面标题（确保网页有显示内容）
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 读取密钥（确保你在 Secrets 里配置了 GEMINI_API_KEY）
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("请在 Streamlit Cloud 的 Secrets 中配置 GEMINI_API_KEY")
    st.stop()

# 3. 上传组件
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='图片上传成功', use_container_width=True)
    
    if st.button("开始识别并计算"):
        with st.spinner('正在通过 Gemini 进行视觉分析...'):
            try:
                # 转换图片格式以适应新版 SDK
                image_bytes = uploaded_file.getvalue()
                
                # 调用模型
                response = client.models.generate_content(
                    model='gemini-2.0-flash', # 请确保使用支持视觉的模型
                    contents=[
                        "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                        {"mime_type": "image/jpeg", "data": image_bytes}
                    ]
                )
                
                # 显示结果
                st.subheader("分析结果")
                st.write(response.text)
                st.info("注：由于未连接数据库，目前显示识别结果，后续可接入 Google Sheets 自动存储。")
                
            except Exception as e:
                st.error(f"分析出错: {e}")
else:
    st.write("请上传图片以开始比价流程。")
