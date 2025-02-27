#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import fitz

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


# In[2]:


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        doc = fitz.open(pdf)
        for page in doc:
            text += page.get_text("text") + "\n"
    return text


# In[3]:


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "],
        length_function=len
    )
    return text_splitter.split_text(text)


# In[4]:


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


# In[5]:


def get_llm():
    llm = ChatOpenAI(
        model='deepseek-chat',
        openai_api_key="YOUR-API-KEY",
        openai_api_base='https://api.deepseek.com',
        temperature=0
    )
    return llm


# In[6]:


def get_chat_memory():
    return ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)


# In[7]:


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


# In[8]:


def create_question_generator():
    llm = get_llm()
    prompt_template = get_prompt_template()
    return LLMChain(llm=llm, prompt=prompt_template)


# In[9]:


def get_conversation_chain(vectorstore):
    question_generator_chain = create_question_generator()
    memory = get_chat_memory()
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=question_generator_chain.llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": question_generator_chain.prompt}
    )
    return conversation_chain


# In[10]:


def load_pdfs_from_folder(folder_path):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]

    print("\n📂 PDFs carregados:")
    for pdf in pdf_files:
        print(f" - {pdf}")
    
    return pdf_files


# In[11]:


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
        
pdf_folder_path = "/home/embs/Downloads/pasta_pdfs_tcc"
chatbot = ChatBotFAQ(pdf_folder_path)


# In[39]:


question = input("Ask me anything about UFRPE and our rules: ")
answer = chatbot.ask_question(question)

print("Resposta:", answer)

