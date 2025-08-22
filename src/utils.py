from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore



# Reading data from PDF function
def load_pdf_files(data):
  loader = DirectoryLoader(
      data,
      glob = '*.pdf',
      loader_cls = PyPDFLoader
  )

  docs = loader.load()
  return docs


# Filter function
def filter_docs(docs:List[Document]) -> List[Document]:
  """The function retains the page content and source, and filters out the rest of the document when provided with a list of documents.
  """
  filtered_docs: List[Document] = []
  for doc in docs:
    src = doc.metadata.get('source')
    filtered_docs.append(
        Document(
            page_content=doc.page_content,
            metadata={'source':src}
        )
    )
  return filtered_docs


# Splitting the documents into smaller chunks
def text_split(filtered_documents):
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 500,
      chunk_overlap = 20
  )
  chunks = text_splitter.split_documents(filtered_documents)
  return chunks

# HuggingFace Embedding
def download_hugging_face_embedding():
# Check for GPU and set the device
  device = 'cuda' if torch.cuda.is_available() else 'cpu'
  print(f"Using device: {device}")

  # The model will download to the new cache location the first time
  embedding = HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L6-v2",
      model_kwargs={'device': device}
  )
  return embedding














