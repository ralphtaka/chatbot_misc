import streamlit as st
from langchain_openai import ChatOpenAI

from simple_logic import SimpleLogic
from langgraph_logic import LanggraphLogic

# for github token
github_token=""

# 如果用一般語言邏輯設定成否，會呼叫SimpleLogic
# 設定成True則啟動laggraph模式
langgraph_logic_flag = True

# 使用使用者最後輸入的幾筆資料拿來判斷情緒，不需要歷史的話請設定為1
user_history_count = 3

def join_last_n_or_all(lst, n, separator):
    return lst[:-n] + [separator.join(lst[-n:])] if len(lst) > n else [separator.join(lst)]

def return_latest_user_history() -> str:
    return join_last_n_or_all(st.session_state.collected_texts, user_history_count,"\n")

def init_session():
    # 初始化 session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "collected_texts" not in st.session_state:
        st.session_state.collected_texts = []

#  簡化流程
def display_message(role, content):
    with st.chat_message(role):
        st.markdown(content)

def display_welcome_message():
    welcome_message = """
    歡迎來到心情點播小工具！
    """
    display_message("assistant", welcome_message)

def display_history():
    display_welcome_message()
    for message in st.session_state.messages:
        display_message(message["role"], message["content"])

def log_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

llm = ChatOpenAI(model="gpt-4o-mini",
                 base_url="https://models.inference.ai.azure.com",
                 api_key=github_token)

# UI 介面標題
st.title("心情DJ陪聊點唱機 - 自動版")

init_session()

# 顯示聊天歷史
display_history()

# 切換邏輯
if langgraph_logic_flag:
    assistant_logic = LanggraphLogic(llm=llm)
else:
    assistant_logic = SimpleLogic(llm=llm)

# 使用者輸入
user_input = st.chat_input("來聊聊吧！")
if user_input:

    # 記錄並顯示使用者訊息
    log_message("user", user_input)
    display_message("user", user_input)

    st.session_state.collected_texts.append(user_input)
    user_history = return_latest_user_history()

    # 預設判斷的輸入歷史是最後三筆
    # 如果不需要最後幾筆的話，可以改成兩個變數都直接用user_input輸入就可以，或者是改上面的數字為1
    response = assistant_logic.assistant_logic(user_input, user_history)

    # 記錄並顯示機器人回應
    log_message("assistant", response)
    display_message("assistant", response)
