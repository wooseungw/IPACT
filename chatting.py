import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from gpt_class import GPT
import time

if "OPENAI_API" not in st.session_state:
    
    st.session_state["OPENAI_API"] = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") else ""
# 기본 모델을 설정합니다.
if "model" not in st.session_state:
    st.session_state["model"] = "gpt-4o"
# 채팅 기록을 초기화합니다.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "sys_prompt" not in st.session_state:
    st.session_state["sys_prompt"] = open("data/prompt_output.txt", "r").read()

st.session_state

def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.04)

if __name__ == '__main__':
    
    st.title("챗-봇")
    # Create a sidebar for API key and model selection
    with st.expander("챗봇 사용법", expanded=False):
        st.markdown("""
                    - 이 챗봇은 사용자의 외로움 종류에 맞는 최적화된 답변을 제공합니다.
                    - 답변의 내용은 사용자의 공감을 위한것이며, 실제로는 존재하지 않는 가상의 챗봇입니다.
                    """)
    ################# 설정을 위한 사이드바를 생성합니다. 여기서 api키를 받아야 실행됩니다. ##########################################
    with st.sidebar:
        st.title("설정")
        st.session_state["OPENAI_API"] = st.text_input("Enter API Key", st.session_state["OPENAI_API"], type="password")
        st.session_state["model"] = st.selectbox("Select Model", ["gpt-4o", "gpt-3.5-turbo"])

    ################## 챗봇을 사용하기 위한 gpt 모델을 정의합니다. ############################################################
    gpt = GPT(api_key=st.session_state["OPENAI_API"], model=st.session_state["model"], sys_prompt = st.session_state["sys_prompt"], top_p=1.0)
    
    ############################################ 실제 챗봇을 사용하기 위한 Streamlit 코드 ###################################################
    for content in st.session_state.chat_history:
        with st.chat_message(content["role"]):
            st.markdown(content['message'])    
    ### 사용자의 입력을 출력하고 생성된 답변을 출력합니다.
    if prompt := st.chat_input("질문을 입력하세요."):
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.chat_history.append({"role": "user", "message": prompt})

        with st.chat_message("ai"):                
            response = gpt.generate(text_prompt = prompt)
            st.write_stream(stream_data(response))
            st.session_state.chat_history.append({"role": "ai", "message": response})