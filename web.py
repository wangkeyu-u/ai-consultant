import streamlit as st
from google import genai
from google.genai import types

# 1. 网页的标题设置
st.title("我的专属商业AI顾问系统")

# 2. 门禁卡（务必替换为你自己的API Key）
my_api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=my_api_key)

my_config = types.GenerateContentConfig(
    system_instruction="你现在是一位顶级的香水品牌商业顾问。除了香水商业相关的问题，你必须直接拒绝回答任何其他话题。"
)

# 3. 在网页上画一个输入框，等待用户打字
user_text = st.text_input("请输入您的问题：")

# 4. 在网页上画一个“发送”按钮
if st.button("发送"):
    # 当按钮被点击，且输入框里有文字时，开始执行AI通讯
    if user_text:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=my_config
        )
        # 5. 把AI传回来的文字，显示在网页上

        st.write(response.text)
