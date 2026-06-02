import streamlit as st
from google import genai  # 使用新导入方式

# 你的 API KEY 设置
api_key = st.secrets["GEMINI_API_KEY"]

# 初始化客户端
client = genai.Client(api_key=api_key)

# 提示：如果使用中转，新版 SDK 配置方式可能不同，建议优先测试直连
# 若必须使用中转，请确保你的中转服务商支持新的 google-genai 库
