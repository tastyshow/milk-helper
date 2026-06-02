import streamlit as st
import time
from google import genai
from PIL import Image

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 初始化客户端
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("配置错误，请检查 Secrets 中的 GEMINI_API_KEY")
    st.stop()

# 3. 文件上传与逻辑
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='图片上传成功', width=300)
    
    if st.button("开始识别"):
        with st.spinner('正在分析中...'):
            try:
                img = Image.open(uploaded_file)
                
                # 使用 gemini-1.5-flash 缓解额度压力
                # 这是一个内置了自动重试逻辑的调用方式
                try:
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=[
                            "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                            img
                        ]
                    )
                except Exception as api_err:
                    if "429" in str(api_err) or "RESOURCE_EXHAUSTED" in str(api_err):
                        st.warning("触发限流，正在等待 30 秒后重试...")
                        time.sleep(30)
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=[
                                "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                                img
                            ]
                        )
                    else:
                        raise api_err
                
                st.subheader("分析结果")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"分析出错: {e}")
                st.write("提示：如果提示 429 错误，说明今日额度已耗尽，请明天重试或检查 Google AI Studio 配额。")
else:
    st.write("请上传图片以开始比价流程。")
