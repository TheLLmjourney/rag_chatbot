from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embedding
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
from pyngrok import ngrok

app = Flask(__name__)

load_dotenv()

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

# Inferencing
openai_api_key = os.getenv('OPEN_AI_API_KEY')

ChatModel = ChatOpenAI(model='gpt-4o-mini-2024-07-18',api_key=openai_api_key)

prompt = ChatPromptTemplate.from_messages(
    [
        ('system',system_prompt),
        ('human','{input}')
    ]
)

# Retriever
retriever = docsearch.as_retriever(search_type='similarity', search_kwargs={'k':3})

# RAG Chain
question_answer_chain = create_stuff_documents_chain(ChatModel,prompt)
rag_chain = create_retrieval_chain(retriever,question_answer_chain)


@app.route('/')
def index():
  return render_template('chat.html')

@app.route('/get', methods=['GET','POST'])
def chat():
  msg = request.form['msg']
  input = msg
  print(input)
  response = rag_chain.invoke({'input':msg})
  print('Response: ', response['answer'])
  return str(response['answer'])

# Running with ngrok

ngrok.kill()

public_url = ngrok.connect(5000)
print(f' * Public URL: {public_url}')
if __name__ == '__main__':
  app.run()
