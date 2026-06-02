import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 初始化 Gemini
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # 强制指定版本，这是最稳妥的调用方式
    genai.configure(api_key=api_key)
    # 使用 1.5-flash，它在所有免费账号下兼容性最好
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"配置错误: {e}")
    st.stop()

# 3. 文件上传
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='图片上传成功', width=300)
    
    if st.button("开始识别并计算"):
        with st.spinner('正在分析中...'):
            try:
                # 将上传的文件转为 PIL Image 对象
                img = Image.open(uploaded_file)
                
                # 发送请求
                response = model.generate_content([
                    "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                    img
                ])
                
                st.subheader("分析结果")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"分析出错: {e}")
                st.write("如果依然 404，请确认你的 API Key 是否在 Google AI Studio 中选择了 'Global' 或 'US' 地区。")
else:
    st.write("请上传图片以开始比价流程。")
