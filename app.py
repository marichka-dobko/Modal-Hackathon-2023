import streamlit as st
import openai
from llmQuery import get_llm_result  # Import the mongoQuery function


def set_custom_css():
    st.markdown(
        """
    <style>
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 1000;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def initialize_session():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_messages():
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        st.write(f"{role.capitalize()}: {content}")


def get_user_input():
    with st.container():
        return st.text_input("What is up?", key="fixed-input")


def process_with_gpt(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    full_response = ""
    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
    st.session_state.messages.append({"role": "assistant", "content": full_response})


def main():
    st.header("Find the right Health Insurance for you")
    set_custom_css()
    initialize_session()

    # Set OpenAI API key
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    user_input = get_user_input()
    if user_input:
        if len(st.session_state.messages) == 0:
            mongo_response = get_llm_result(user_input)
            print('Were here')
            st.session_state.messages.append({"role": "assistant", "content": str(mongo_response)})
        else:
            process_with_gpt(user_input)

    display_messages()

if __name__ == "__main__":
    main()
