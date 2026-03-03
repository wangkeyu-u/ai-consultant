import streamlit as st
from google import genai
from google.genai import types

st.title("我的专属商业AI顾问系统")

# 1. 基础配置（不变）
my_api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=my_api_key)
my_config = types.GenerateContentConfig(
    system_instruction="你现在是一位顶级的香水品牌商业顾问。除了香水商业相关的问题，你必须直接拒绝回答任何其他话题。"
)

# 2. 核心逻辑：建立并锁定“AI记忆盒子”
# 客观判断：如果保险箱（session_state）里没有叫 'chat' 的盒子，就新建一个放进去。
# 如果已经有了，代码每次重新跑的时候就会跳过这一步，从而保住记忆。
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model='gemini-2.5-flash',
        config=my_config
    )

# 3. 建立并锁定“网页显示用的聊天记录本”
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 每次代码重新跑的时候，先把保险箱里的历史记录像画气泡一样画在屏幕上
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# 5. 现代化的底部聊天输入框
user_text = st.chat_input("请输入您的商业问题...")

# 6. 触发器：如果用户敲击了回车键发送文字
if user_text:
    # 步骤 A：把用户的话画在屏幕上，并存进保险箱
    with st.chat_message("user"):
        st.write(user_text)
    st.session_state.messages.append({"role": "user", "text": user_text})
    
    # 步骤 B：动用保险箱里那个带记忆的 AI 去发送问题
    response = st.session_state.chat.send_message(user_text)
    
    # 步骤 C：把 AI 的回答画在屏幕上，并存进保险箱
    with st.chat_message("assistant"):
        st.write(response.text)
    st.session_state.messages.append({"role": "assistant", "text": response.text})
