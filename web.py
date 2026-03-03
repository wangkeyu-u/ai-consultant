import streamlit as st
from google import genai
from google.genai import types

st.title("我的专属商业AI顾问系统")

# 从云端保险箱读取钥匙
my_api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=my_api_key)

my_config = types.GenerateContentConfig(
    system_instruction="你现在是一位顶级的香水品牌商业顾问。除了香水商业相关的问题，你必须直接拒绝回答任何其他话题。"
)

user_text = st.text_input("请输入您的问题：")

if st.button("发送"):
    if user_text:
        # 【核心改动】：植入 try-except 探针
        try:
            # 尝试执行危险通讯动作
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_text,
                config=my_config
            )
            st.write(response.text)
        except Exception as e:
            # 如果通讯失败，强行拦截底层死因，并用红色警告框显示在网页上
            st.error(f"致命错误捕获：{e}")
