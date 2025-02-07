import streamlit as st
from langchain.memory import ConversationBufferMemory
from backend import get_chat_response


def initialize_session_state():
    """初始化会话状态"""
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
        st.session_state["messages"] = [{"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]


def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
        st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

        if st.button("清空对话"):
            st.session_state["messages"] = [{"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]
            st.session_state["memory"].clear()
            st.success("对话已清空！")
    return openai_api_key


def render_chat_messages():
    """渲染聊天消息"""
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])


def handle_user_input(openai_api_key):
    """处理用户输入并获取AI响应"""
    prompt = st.chat_input()
    if prompt:
        if not openai_api_key:
            st.info("请输入OpenAI API Key以继续。")
            st.stop()

        if not openai_api_key.startswith("sk-"):
            st.error("API Key格式不正确，请检查后重新输入。")
            st.stop()

        st.session_state["messages"].append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)

        try:
            with st.spinner("AI正在思考中，请稍等..."):
                response = get_chat_response(prompt, st.session_state["memory"], openai_api_key)

            msg = {"role": "ai", "content": response}
            st.session_state["messages"].append(msg)
            st.chat_message("ai").write(response)
        except Exception as e:
            st.error(f"发生错误：{str(e)}")


def main():
    """主函数"""
    st.set_page_config(page_title="克隆ChatGPT", layout="wide")
    st.title("克隆ChatGPT")
    initialize_session_state()
    openai_api_key = render_sidebar()
    render_chat_messages()
    handle_user_input(openai_api_key)


if __name__ == "__main__":
    main()