import os
from flask import Flask, render_template, jsonify, request
from src.utils import download_hugging_face_embedding
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from src.prompt import *
from pyngrok import ngrok

import json
from uuid import uuid4
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from pinecone import Pinecone
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory



# --- Core Flask App Setup ---
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Get API keys
pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPEN_AI_API_KEY')

os.environ['PINECONE_API_KEY'] = pinecone_api_key
os.environ['OPENAI_API_KEY'] = openai_api_key


# Embedding
embedding = download_hugging_face_embedding()

# VectorStore
index_name = 'rag-chatbot'

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)

# Retriever
retriever = docsearch.as_retriever(search_type='similarity', search_kwargs={'k': 3})

# Inferencing
ChatModel = ChatOpenAI(model='gpt-4o-mini-2024-07-18', api_key=openai_api_key)

# GPT corrections
# --- prompts ---
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "Given the chat history and the latest user question, rewrite it as a standalone, specific question. "
         "Do NOT answer; only rewrite the question."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(ChatModel, retriever, contextualize_q_prompt)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a helpful RAG assistant. Use chat history to resolve references and maintain continuity. "
         "Ground factual answers in the retrieved context below:\n\n{context}\n\n"
         "If the answer isn't in the context, say you don't know."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)


# RAG Chain
question_answer_chain = create_stuff_documents_chain(ChatModel, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# --- History Management ---
from langchain_community.chat_message_histories import FileChatMessageHistory

# Ensure directory exists
os.makedirs("histories", exist_ok=True)

def get_session_history(session_id: str):
    """
    Retrieves a persistent FileChatMessageHistory for a given session ID.
    This ensures chat history is saved to disk and survives reloads.
    """
    return FileChatMessageHistory(f"histories/{session_id}.json")


# --- History wrapper (with correct output_messages_key) ---
with_message_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# --- Flask Routes ---

@app.route('/')
def index():
    # Pass a new session ID to the template for a fresh conversation
    return render_template('index.html', session_id=str(uuid4()))  # <-- str()

@app.route('/get', methods=['POST'])
def chat():
    msg = request.form.get('msg', '').strip()
    session_id = request.form.get('session_id') or str(uuid4())

    print(f"\nUser with session ID '{session_id}' asked: {msg}")

    # Run the chain with memory
    response = with_message_history.invoke(
        {"input": msg},
        config={"configurable": {"session_id": session_id}}
    )

    # Debug: show history in console
    history = get_session_history(session_id).messages
    print("📜 Conversation so far:")
    for turn in history:
        who = "Human" if turn.type == "human" else "AI"
        print(f"  {who}: {turn.content}")
    print("🤖 Response:", response['answer'], "\n")

    return str(response['answer'])


# Running with ngrok

ngrok.kill()

public_url = ngrok.connect(5000)
print(f' * Public URL: {public_url}')
if __name__ == '__main__':
  app.run()
