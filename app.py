import streamlit as st
from google import genai
from google.genai import types

# 1. 页面配置
st.set_page_config(page_title="牛奶比价助手", layout="centered")
st.title("🥛 牛奶比价记录助手")

# 2. 读取 Secrets 中的 API KEY
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("未检测到 API KEY，请在 Streamlit Cloud 的 Secrets 中配置 GEMINI_API_KEY")
    st.stop()

# 3. 文件上传组件
uploaded_file = st.file_uploader("请上传牛奶标签截图", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 显示已上传图片
    st.image(uploaded_file, caption='图片上传成功', width='stretch')
    
    if st.button("开始识别并计算"):
        with st.spinner('正在通过 Gemini 进行视觉分析...'):
            try:
                # 获取二进制数据
                image_bytes = uploaded_file.getvalue()
                
                # 使用 types.Part 封装图片数据 (新版 SDK 标准)
                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                )
                
                # 调用模型
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[
                        "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                        image_part
                    ]
                )
                
                # 显示结果
                st.subheader("分析结果")
                st.write(response.text)
                st.info("注：识别已完成，您可以根据识别出的数据进行手动或后续接入记录。")
                
            except Exception as e:
                st.error(f"分析出错: {e}")
                st.write("请检查 API KEY 是否有效，或者图片是否过于模糊。")
else:
    st.write("请上传图片以开始比价流程。")
