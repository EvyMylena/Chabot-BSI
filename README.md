# 🤖 ChatBot BSI UFRPE

Este é um chatbot desenvolvido para responder dúvidas frequentes sobre o curso de **Bacharelado em Sistemas de Informação (BSI)** da **Universidade Federal Rural de Pernambuco (UFRPE)**. Ele utiliza processamento de linguagem natural e aprendizado de máquina para fornecer respostas com base em documentos oficiais da instituição.

---

## 📚 Funcionalidades

- ✅ Leitura e indexação de documentos PDF com normas e regulamentos do curso.
- ✅ Respostas baseadas exclusivamente no conteúdo dos documentos carregados.
- ✅ Memória de conversa para contextualização de perguntas anteriores.
- ✅ Interface amigável via [Streamlit](https://streamlit.io).

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- [LangChain](https://www.langchain.com/)
- [HuggingFace Embeddings](https://huggingface.co/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Streamlit](https://streamlit.io/)
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [ChatOpenAI (DeepSeek)](https://deepseek.com/)

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/chatbot-bsi-ufrpe.git
cd chatbot-bsi-ufrpe

---

### 2. Crie um ambiente virtual

python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

---

### 3. Instale as dependências

pip install -r requirements.txt

---

### 4. Configure sua API Key

openai_api_key="sk-..." # substitua pela sua chave do deepseek no arquivo chatbot.py

---

### 5. Rode a aplicação

streamlit run app.py
