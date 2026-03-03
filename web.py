import streamlit as st
from google import genai
from google.genai import types

st.title("我的专属商业AI顾问系统")

my_config = types.GenerateContentConfig(
    system_instruction="你现在是一位顶级的香水品牌商业顾问。除了香水商业相关的问题，你必须直接拒绝回答任何其他话题。"
)

# 核心修复：把通讯器（client）和记忆盒子（chat）作为一个整体，全部锁进保险箱
if "client" not in st.session_state:
    # 1. 在保险箱里打造专属通讯器
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    # 2. 强制要求记忆盒子使用保险箱里的这个通讯器
    st.session_state.chat = st.session_state.client.chats.create(
        model='gemini-2.5-flash',
        config=my_config
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

user_text = st.chat_input("请输入您的商业问题...")

if user_text:
    # 打印并存储用户的提问
    with st.chat_message("user"):
        st.write(user_text)
    st.session_state.messages.append({"role": "user", "text": user_text})
    
    # 使用保险箱里的记忆盒子发送消息（此时它的通讯器绝对不会断开）
    response = st.session_state.chat.send_message(user_text)
    
    # 打印并存储AI的回答
    with st.chat_message("assistant"):
        st.write(response.text)
    st.session_state.messages.append({"role": "assistant", "text": response.text})

