import streamlit as st
from google import genai
from google.genai import types

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 初始化客户端 (采用最基础的配置)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # 删掉所有额外的 http_options 配置，让 SDK 使用默认环境配置
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("配置错误，请检查 Secrets 中的 GEMINI_API_KEY")
    st.stop()

# 3. 文件上传组件
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='图片上传成功', width='stretch')
    
    if st.button("开始识别并计算"):
        with st.spinner('正在通过 Gemini 进行视觉分析...'):
            try:
                image_bytes = uploaded_file.getvalue()
                
                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                )
                
                # 【关键修复】：使用最简化的模型 ID
                # 某些 API 环境下，必须使用 gemini-1.5-flash，不能加任何后缀
                response = client.models.generate_content(
                    model='gemini-1.5-flash', 
                    contents=[
                        "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                        image_part
                    ]
                )
                
                st.subheader("分析结果")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"分析出错: {e}")
                st.write("如果依然显示 404，建议检查你的 Google Cloud Project 是否已在该区域开通了该模型的访问权限。")
else:
    st.write("请上传图片以开始比价流程。")
