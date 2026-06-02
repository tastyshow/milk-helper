import streamlit as st
import time
from google import genai
from PIL import Image

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 纯净初始化
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # 不使用任何特殊配置，直接连接
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"密钥加载失败: {e}")
    st.stop()

# 3. 核心逻辑
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, width=300)
    
    if st.button("开始分析"):
        with st.spinner('正在分析中...'):
            try:
                img = Image.open(uploaded_file)
                
                # 【终极调整】：强制使用模型 ID 的基本名称，不带任何路径前缀
                # 某些环境下 Google SDK 对 models/ 前缀极其敏感
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=[
                        "请识别价格和容量，计算折合250ml的价格。格式：价格:X, 容量:Y, 折合250ml:Z。",
                        img
                    ]
                )
                
                st.subheader("分析结果")
                st.write(response.text)
                
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg:
                    st.error("404 错误：模型未找到。")
                    st.write("诊断建议：你的 API Key 可能绑定了一个没有模型访问权限的旧项目。请前往 AI Studio 创建一个全新的 API Key，不要使用 Default 项目。")
                elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    st.warning("额度已耗尽 (429)，请明天再试。")
                else:
                    st.error(f"分析出错: {e}")

else:
    st.write("请上传图片以开始比价流程。")
