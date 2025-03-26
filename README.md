# 🤖 ChatBot BSI UFRPE

Este é um chatbot foi desenvolvido para o Trabalho de Conclusão do curso de **Bacharelado em Sistemas de Informação (BSI)** da **Universidade Federal Rural de Pernambuco (UFRPE)** com a finalidade responder perguntas frequentes dos alunos. Ele utiliza processamento de linguagem natural e aprendizado de máquina para fornecer respostas com base em documentos oficiais da instituição.

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

## 📁 Estrutura do Projeto

chatbot-bsi-ufrpe/
│
├── streamlit-app.py # Interface principal com o usuário (Streamlit)
├── chatbot.py # Lógica de processamento e resposta do chatbot
├── requirements.txt # Lista de dependências
├── README.md
└── pdfs/ # Pasta contendo os PDFs com as normas da UFRPE
    ├── regulamento.pdf # exemplos
    └── tcc-normas.pdf

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/chatbot-bsi-ufrpe.git
cd chatbot-bsi-ufrpe
```

---

### 2. Crie um ambiente virtual

```bash
💻 No Linux/macOS:

python3 -m venv venv
source venv/bin/activate

🪟 No Windows:

python -m venv venv
venv\Scripts\activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configure sua API Key

```bash
openai_api_key="sk-..." # substitua pela sua chave do deepseek no arquivo chatbot.py
```

---

### 5. Rode a aplicação

```bash
streamlit run app.py
```

## 🧠 Exemplos de perguntas que o ChatBot pode responder
- Quais são as regras para trancamento de disciplina?
- Qual a carga horária mínima por semestre?
- Como funcionam os estágios supervisionados?

## 📌 Observações
- O chatbot não gera respostas fora dos documentos carregados.
- Garanta que os PDFs estejam bem estruturados e legíveis para melhor desempenho.

## 👨‍💻 Autor
Desenvolvido por [Evelyn Mylena Bezerra e Silva] para o Trabalho de Conclusão de Curso - BSI/UFRPE.
