import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from gpt_class import GPT
import time
import json

class User:
    def __init__(self, info_dir):
        # Read the JSON file
        with open(info_dir, 'r') as file:
            data = json.load(file)
        self.name = data['personal_information']['name']
        self.age = data['personal_information']['age']
        self.gender = data['personal_information']['gender']
        self.merry = data['personal_information']['merry']
        self.children = data['personal_information']['children']
        self.religion = data['personal_information']['religion']
        self.economy_states = data['personal_information']['economy_states']
        self.health_states = data['personal_information']['health_states']
        self.living_arrangement = data['personal_information']['living_arrangement']        
# Specify the path to the JSON file
info_dir = 'data/ipact_personal_main/data3.json'
user = User(info_dir)

if "OPENAI_API" not in st.session_state:
    st.session_state["OPENAI_API"] = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") else ""
# 기본 모델을 설정합니다.
if "model" not in st.session_state:
    st.session_state["model"] = "gpt-4o"
# 채팅 기록을 초기화합니다.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "sys_prompt" not in st.session_state:
    with open("data/prompt_output.txt", "r") as file:
        sys_prompt = file.read()
    print(sys_prompt)
    personal_info="""
    #설문지 인적 정보 양식
    본 설문지의 인적 정보의 답변 값에 대한 숫자와 값을 일치시켰습니다. 괄호 안의 값을 참고하세요
    이름(name) : 00
    연령(age) : 0(65-74세) / 1(75-84세) / 2(85세 이상)
    성별(gender) : male / female
    결혼 상태(merry) : 0(미혼) / 1(기혼) / 2(이혼/별거) / 3(사별)
    거주 형태(living_arrangement) : 0(혼자 거주) / 1(동거)
    자녀 수 (chlidren) : 0(없음) / 2(1-2명) / 3(3명 이상)
    종교(religion): 1(있음) / 0(없음)
    지각된 경제 상태(economy_states): 0(나쁨) / 1(보통) / 2(좋음)
    지각된 건강 상태(health_states): 0(나쁨) / 1(보통) / 2(좋음)
    """
    st.session_state["sys_prompt"] = sys_prompt + personal_info+f"""
        사용자의 인적정보 = 이름: {user.name},
        나이: {user.age}, 
        성별: {user.gender}, 
        결혼 여부: {user.merry}, 
        자녀 수: {user.children}, 
        종교: {user.religion}, 
        거주 형태: {user.living_arrangement},
        인지된 경제 상태: {user.economy_states}, 
        인지된 건강 상태: {user.health_states},
        
        \\
    """
    print(st.session_state["sys_prompt"])

def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.04)
#
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