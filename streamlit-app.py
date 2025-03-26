import os
import streamlit as st
from chatbot import ChatBotFAQ 

st.set_page_config(page_title="Chatbot BSI UFRPE", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .stChatMessage.assistant {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .stTextInput input {
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
</style>
""", unsafe_allow_html=True)

st.title("Smart Chatbot do Curso de BSI da UFRPE")
st.write("Bem-vindo ao ChatBot do curso de Bacharelado em Sistemas de Informação da UFRPE. Faça perguntas sobre regras, disciplinas, programas e mais!")

pdf_folder_path = "pdfs"
if not os.path.exists(pdf_folder_path):
    st.error(f"Pasta '{pdf_folder_path}' não encontrada. Certifique-se de que os PDFs estão na pasta correta.")
    st.stop()

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBotFAQ(pdf_folder_path)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o ChatBot do curso de BSI da UFRPE. Como posso ajudar você hoje?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Digite sua pergunta aqui"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Processando sua pergunta..."):
        answer = st.session_state.chatbot.ask_question(prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
