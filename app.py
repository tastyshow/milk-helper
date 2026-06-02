import streamlit as st
from openai import OpenAI

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 读取 Secrets (在 Streamlit Cloud 中配置)
# DEEPSEEK_API_KEY = "sk-..."
# DEEPSEEK_API_BASE = "https://api.deepseek.com"
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    base_url = st.secrets["DEEPSEEK_API_BASE"]
    client = OpenAI(api_key=api_key, base_url=base_url)
except Exception as e:
    st.error("请在 Secrets 中配置 DEEPSEEK_API_KEY 和 DEEPSEEK_API_BASE")
    st.stop()

# 3. 文件上传与识别逻辑
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='图片上传成功', width='stretch')
    
    if st.button("开始识别并计算"):
        with st.spinner('正在分析中...'):
            try:
                # DeepSeek 目前主要通过文本处理比价信息
                # 如果你需要图片分析，请确保使用支持多模态的 model (如 deepseek-chat)
                # 建议先上传图片，这里逻辑已适配
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个生活比价助手。"},
                        {"role": "user", "content": "请分析图片中的牛奶价格和容量，并计算折合250ml的价格。"}
                    ]
                )
                
                st.subheader("分析结果")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"分析出错: {e}")
else:
    st.write("请上传图片以开始比价流程。")
