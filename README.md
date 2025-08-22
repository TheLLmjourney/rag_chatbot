# 🧠 RAG Chatbot with Persistent Memory (Flask + LangChain + Pinecone)

## 📌 Overview
This project is a **Retrieval-Augmented Generation (RAG) chatbot** built with:
- **Flask** for the backend API
- **Custom HTML/CSS/JavaScript** frontend (Streamlit-free)
- **LangChain** for orchestration
- **Pinecone** as the vector store
- **OpenAI GPT (gpt-4o-mini)** as the LLM
- **FileChatMessageHistory** for persistent conversation memory

The chatbot:
1. **Rewrites follow-up questions** into standalone queries (contextualizer).
2. **Retrieves relevant documents** from Pinecone.
3. **Maintains session-based memory** (chat history saved as JSON).
4. **Provides a clean full-stack UI** built without Streamlit.

---

## ⚙️ Architecture
<img width="861" height="1111" alt="rag_chatbot drawio (2)" src="https://github.com/user-attachments/assets/06a528da-c70d-4654-b5bc-18ac979a2239" />

---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Flask, Python  
- **LLM:** OpenAI GPT (via LangChain)  
- **Vector DB:** Pinecone  
- **Memory:** FileChatMessageHistory (LangChain)  

---

## .env file for RAG Chatbot
## Set these keys in your root project folder.
### OpenAI API Key
OPEN_AI_API_KEY=your_openai_api_key_here

### Pinecone API Key
PINECONE_API_KEY=your_pinecone_api_key_here

### Grok API Key (optional)
GROK_API_KEY=your_grok_api_key_here

---

## 📚 What I Learned
- Started learning JavaScript to build an interactive chat UI.  
- Learned how to separate frontend (HTML/CSS/JS) and backend (Flask) for clean structure.  
- Understood the role of query contextualization and memory in RAG pipelines.  
- Gained experience integrating Pinecone, OpenAI, and LangChain into a Flask app.


