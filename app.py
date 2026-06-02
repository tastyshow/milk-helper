from google import genai
from google.genai import types  # 必须导入这个用于封装图片

# ... (前面代码不变)

    if st.button("开始识别并计算"):
        with st.spinner('正在通过 Gemini 进行视觉分析...'):
            try:
                # 获取二进制数据
                image_bytes = uploaded_file.getvalue()
                
                # 【关键修复】使用 types.Part 封装图片数据
                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                )
                
                # 调用模型（传入文本提示和封装好的图片部分）
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[
                        "请识别图片中的牛奶价格和容量。计算出折合 250ml 的价格。输出格式：价格:X元, 容量:Yml, 折合250ml价格:Z元。",
                        image_part
                    ]
                )
                
                st.subheader("分析结果")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"分析出错: {e}")
