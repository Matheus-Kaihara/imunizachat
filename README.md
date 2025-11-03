# 💉 Imunizachat

Course Completion Project (TCC - Trabalho de Conclusão de Curso) 🎓
This project involves the development of a web system 🌐 that provides information about vaccines 💉 through an intelligent chatbot 🤖 built using neural networks, a Large Language Model (LLM) 🧠, and a web scraper 🕷️.

## 🚀 Features

🧠 AI-powered chatbot for answering questions about vaccines.

🌐 Web interface for easy interaction.

🕷️ Automated web scraping to gather up-to-date vaccine information.

💾 Backend integration with APIs and databases.

🔒 Secure data handling and scalable architecture.

## 🛠️ Technologies Used

⚙️ Python (FastAPI, asyncio, BeautifulSoup, etc.)

🤖 Machine Learning / LLMs (e.g., OpenAI, Transformers)

🗃️ Database (PostgreSQL / MongoDB)

🌐 Frontend (React, HTML, CSS, JavaScript)

🧰 Tools: Git, Docker, VSCode

## ▶️ Como executar o ImunizaChat

1. Crie um arquivo `.env` na raiz com a sua `OPENAI_API_KEY` (veja `env.example`).
2. Instale as dependências Python:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o coletor de documentos (opcional) para popular a base vetorial:

   ```bash
   python insert_docs.py <URL>
   ```

4. Inicie a API FastAPI do ImunizaChat:

   ```bash
   uvicorn api:app --reload
   ```

   O serviço ficará disponível em `http://localhost:8000`.

5. Abra o frontend em `frontend/index.html` (por exemplo usando a extensão **Live Server** do VS Code).

   O HTML contém um `chatbot-container` que conversa com o backend através da rota `/chat` e mantém o histórico por sessão.

> ⚠️ Certifique-se de que o banco vetorial em `./chroma_db` esteja criado antes de conversar com o agente, caso contrário ele responderá somente com conhecimento geral.
