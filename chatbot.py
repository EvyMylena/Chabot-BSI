import os
import fitz
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        doc = fitz.open(pdf)
        for page in doc:
            text += page.get_text("text") + "\n"
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
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
        openai_api_key="sk-...",  # your-api-key
        openai_api_base='https://api.deepseek.com',
        temperature=0
    )
    return llm


def get_chat_memory():
    return ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True, output_key="answer")


def get_prompt_template():
    prompt_text = """
    You are a university assistant. Coordinators or students will ask questions about rules, 
    workload, courses, course registration, and other topics related to the Federal Rural University of Pernambuco 
    and its programs. Respond exclusively based on the provided documents, ignoring any irrelevant context.

    Context: {context}
    Question: {question}
    Answer:
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
        combine_docs_chain_kwargs={"prompt": question_generator_chain.prompt},
        return_source_documents=True
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
