import streamlit as st
from streamlit_chat import message
import google.generativeai as palm
from langchain.llms import GooglePalm
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import boto3
from botocore.exceptions import ClientError

def get_secret_key():
    ssm = boto3.client('ssm', region_name='us-east-1')  
    parameter_name = '/your/app/secret-key'  
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

secret_key = get_secret_key()

st.session_state.messages = [] 

def get_palm_api_key():
    try:
        ssm = boto3.client('ssm', region_name='us-east-1')  
        response = ssm.get_parameter(Name='/homework-helper/palm-api-key', WithDecryption=True)
        return response['Parameter']['Value']
    except ClientError as e:
        st.error(f"Failed to retrieve PaLM API key: {e}")
        return None

palm_api_key = get_palm_api_key()

template = """
**Homework Helper Chatbot**

Welcome to the homework helper chatbot! I'm here to help you with your homework questions. Please feel free to ask me anything about your schoolwork.

**Previous Conversation:**

{history}

**Your Question:**

Human: {human_input}

**AI Response:**

AI: """

memory = ConversationBufferMemory(max_message_count=100)
prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
llm = GooglePalm(google_api_key=palm_api_key)
llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

st.title("Homework-Helper")
st.balloons()

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt = a.text_input(
        label="Your question or task:",
        placeholder="Ask me anything! I'm your virtual homework buddy, ready to help...",
        label_visibility="collapsed",
    )

    b.form_submit_button("Send", use_container_width=True)

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

if user_prompt and palm_api_key:

    palm.configure(api_key=palm_api_key)  

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    message(user_prompt, is_user=True)

    response = llm_chain.run(user_prompt)  # get response from PaLM llm_chain

    msg = {"role": "assistant", "content": response}
    st.session_state.messages.append(msg)  
    message(msg["content"])  # display message on the screen

def clear_chat():
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to your homework helper! I'm here to assist you with your schoolwork"}]

if len(st.session_state.messages) > 1:
    st.button('Clear Chat', on_click=clear_chat)
