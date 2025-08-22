import os
from dotenv import load_dotenv
import pinecone
from src.utils import load_pdf_files, filter_docs, text_split, download_hugging_face_embedding
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv('OPEN_AI_API_KEY')

os.environ['PINECONE_API_KEY'] = pinecone_api_key
os.environ['OPENAI_API_KEY'] = openai_api_key


# Data Ingestion
extracted_data = load_pdf_files(data='data/')
filtered_data = filter_docs(extracted_data)
text_chunks = text_split(filtered_data)


# Embedding Data
embedding = download_hugging_face_embedding()


# Vector Database
pc = Pinecone(api_key=pinecone_api_key)

index_name = 'rag-chatbot'

if not pc.has_index(index_name):
  pc.create_index(
      name = index_name,
      dimension = 384,
      metric = 'cosine',
      spec = ServerlessSpec(cloud='aws', region='us-east-1')
  )

index = pc.Index(index_name)

# Loading Existing Index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embedding,
    index_name=index_name
)












