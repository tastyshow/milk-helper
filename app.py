import streamlit as st
from google import genai

# 设置页面
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 读取密钥
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("请在 Streamlit Cloud 的 Secrets 中配置 GEMINI_API_KEY")
    st.stop()

# 上传组件
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 修复：将 use_container_width=True 改为 width='stretch'
    st.image(uploaded_file, caption='图片上传成功', width='stretch')
    
    if st.button("开始识别并计算"):
        with st.spinner('正在通过 Gemini 进行视觉分析...'):
            try:
                image_bytes = uploaded_file.getvalue()
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[
                        "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                        {"mime_type": "image/jpeg", "data": image_bytes}
                    ]
                )
                
                st.subheader("分析结果")
                st.write(response.text)
                st.info("注：识别已完成。")
                
            except Exception as e:
                st.error(f"分析出错: {e}")
else:
    st.write("请上传图片以开始比价流程。")
