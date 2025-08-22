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


