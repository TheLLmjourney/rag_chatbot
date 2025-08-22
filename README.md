# 🧠 RAG Chatbot with Persistent Memory (Flask + LangChain + Pinecone)

## 📌 Overview
This project is a **Retrieval-Augmented Generation (RAG) chatbot** built with:
- **Flask** for the backend API
- **Custom HTML/CSS/JavaScript** frontend (Streamlit-free)
- **LangChain** for orchestration
- **Pinecone** as the vector store
- **OpenAI GPT (gpt-4o-mini)** as the LLM
- **FileChatMessageHistory** for persistent conversation memory

Unlike simple RAG demos, this chatbot:
1. **Rewrites follow-up questions** into standalone queries (contextualizer).
2. **Retrieves relevant documents** from Pinecone.
3. **Maintains session-based memory** (chat history saved as JSON).
4. **Provides a clean full-stack UI** built without Streamlit.

---

## ⚙️ Architecture

![alt text](https://github.com/user-attachments/files/21937059/rag_chatbot.tif)
