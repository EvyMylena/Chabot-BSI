#!/usr/bin/env python
# coding: utf-8

import os
import fitz
import streamlit as st

from PyPDF2 import PdfReader
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from sentence_transformers import SentenceTransformer


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        doc = fitz.open(pdf)
        for page in doc:
            text += page.get_text("text") + "\n"
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "],
        length_function=len
    )
    return text_splitter.split_text(text)


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


def get_llm():
    llm = ChatOpenAI(
        model='deepseek-chat',
        openai_api_key='DEEPSEEK_API_KEY',
        openai_api_base='https://api.deepseek.com',
        temperature=0
    )
    return llm


def get_chat_memory():
    return ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)


def get_prompt_template():
    prompt_text = """
    You are a university assistant. Coordinators or students will ask questions about rules, 
    workload, courses, course registration, and other topics related to the Federal Rural University of Pernambuco 
    and its programs. Respond exclusively based on the provided documents, ignoring any irrelevant context.

    Contexto: {context}
    Pergunta: {question}
    Resposta:
    """

    return ChatPromptTemplate.from_template(prompt_text)


def create_question_generator():
    llm = get_llm()
    prompt_template = get_prompt_template()
    return LLMChain(llm=llm, prompt=prompt_template)


def get_conversation_chain(vectorstore):
    question_generator_chain = create_question_generator()
    memory = get_chat_memory()

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=question_generator_chain.llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": question_generator_chain.prompt}
    )
    return conversation_chain


def load_pdfs_from_folder(folder_path):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    return pdf_files


class ChatBotFAQ:
    def __init__(self, pdf_folder_path):
        pdf_files = load_pdfs_from_folder(pdf_folder_path)
        raw_text = get_pdf_text(pdf_files)
        text_chunks = get_text_chunks(raw_text)
        self.vectorstore = get_vectorstore(text_chunks)

        self.conversation_chain = get_conversation_chain(self.vectorstore)
        self.memory = get_chat_memory()

    def ask_question(self, question):
        response = self.conversation_chain({"question": question, "chat_history": self.memory.buffer})
        return response["answer"]


# Configuração do Streamlit
st.set_page_config(page_title="Chatbot BSI UFRPE", page_icon="🤖", layout="wide")

# Estilos personalizados
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

# Título e descrição
st.title("Smart Chatbot do Curso de BSI da UFRPE")
st.write("Bem-vindo ao ChatBot do curso de Bacharelado em Sistemas de Informação da UFRPE. Faça perguntas sobre regras, disciplinas, programas e mais!")

# Carregar PDFs
pdf_folder_path = ("./pdfs")
if not os.path.exists(pdf_folder_path):
    st.error(f"Pasta '{pdf_folder_path}' não encontrada. Certifique-se de que os PDFs estão na pasta correta.")
    st.stop()

# Inicializar o chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatBotFAQ(pdf_folder_path)

# Inicializar o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o ChatBot do curso de BSI da UFRPE. Como posso ajudar você hoje?"}
    ]

# Exibir o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo de entrada para a pergunta
if prompt := st.chat_input("Digite sua pergunta aqui"):
    # Adicionar a pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Processar a pergunta e obter a resposta
    with st.spinner("Processando sua pergunta..."):
        answer = st.session_state.chatbot.ask_question(prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Exibir a resposta do chatbot
    with st.chat_message("assistant"):
        st.write(answer)
