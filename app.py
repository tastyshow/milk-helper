import streamlit as st
from google import genai
from google.genai import types

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 读取 API KEY
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("未配置 API KEY，请在 Streamlit Cloud 的 Secrets 中设置 GEMINI_API_KEY")
    st.stop()

# 3. 文件上传组件
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='图片上传成功', width='stretch')
    
    if st.button("开始识别并计算"):
        with st.spinner('正在分析中...'):
            try:
                image_bytes = uploaded_file.getvalue()
                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                )
                
                # 【修改点】：切换为 gemini-1.5-flash 以缓解额度压力
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
                st.error(f"分析出错 (错误代码 {type(e).__name__}): {e}")
                st.write("提示：如果提示额度耗尽，请更换 API Key 或明天重试。")
else:
    st.write("请上传图片以开始比价流程。")
