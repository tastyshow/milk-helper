import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. 页面设置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 检查配置
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 使用标准模型名称
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"配置错误: {e}")
    st.stop()

# 3. 文件处理
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='图片上传成功', width='stretch')
    
    if st.button("开始识别"):
        with st.spinner('正在分析中...'):
            try:
                img = Image.open(uploaded_file)
                # 直接调用模型
                response = model.generate_content([
                    "请识别图片中的牛奶价格和容量，计算折合250ml的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。", 
                    img
                ])
                st.subheader("分析结果")
                st.write(response.text)
            except Exception as e:
                st.error(f"分析出错: {e}")
                st.info("如果还是 404，请确保 API Key 在 AI Studio 中是针对此项目激活的。")
