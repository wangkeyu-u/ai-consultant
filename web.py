import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader  # 新增：导入 PDF 读取工具

st.title("高级商业AI：PDF 知识库顾问")

# 1. 基础配置与安全锁
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    st.session_state.messages = []
    # 初始化一个空的知识库盒子
    st.session_state.pdf_context = ""

# --- 侧边栏：文件上传区 ---
with st.sidebar:
    st.header("知识库上传")
    uploaded_file = st.file_uploader("上传 PDF 文件", type="pdf")
    
    if uploaded_file:
        # 物理读取：将 PDF 转换为文字
        reader = PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
        
        # 存入保险箱，并提示成功
        st.session_state.pdf_context = full_text
        st.success("文件已解析，AI 已进入‘开卷模式’")

# --- 核心 AI 逻辑 ---
# 动态生成系统指令：如果上传了文件，就命令 AI 参考文件内容
base_instruction = "你现在是一位顶级的商业顾问。"
if st.session_state.pdf_context:
    base_instruction += f"\n\n【核心参考资料】：\n{st.session_state.pdf_context}\n\n请优先根据资料回答。"

my_config = types.GenerateContentConfig(system_instruction=base_instruction)

# 确保记忆盒子存在
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model='gemini-2.5-flash',
        config=my_config
    )

# 渲染对话气泡
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# 聊天输入
user_text = st.chat_input("请基于文档向我提问...")

if user_text:
    with st.chat_message("user"):
        st.write(user_text)
    st.session_state.messages.append({"role": "user", "text": user_text})
    
    # 向 AI 发送请求
    response = st.session_state.chat.send_message(user_text)
    
    with st.chat_message("assistant"):
        st.write(response.text)
    st.session_state.messages.append({"role": "assistant", "text": response.text})

