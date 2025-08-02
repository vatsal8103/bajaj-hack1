import os
import pinecone
from langchain_community.vectorstores import Pinecone as LC_Pinecone
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_chunks(text, chunk_size=800, chunk_overlap=80):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def embed_and_store(texts, index_name="insurance-policy"):
    embeddings = OpenAIEmbeddings()
    if index_name not in pinecone.list_indexes():
        # 'dimension=1536' is correct for OpenAI-type embeddings; change if you use a different embedder
        pinecone.create_index(name=index_name, dimension=1536, metric="cosine")
    vstore = LC_Pinecone.from_texts(
        texts=texts if isinstance(texts, list) else [texts],
        embedding=embeddings,
        index_name=index_name
    )
    return vstore

def get_vectorstore(index_name="insurance-policy"):
    embeddings = OpenAIEmbeddings()
    index = pinecone.Index(index_name)
    return LC_Pinecone(index, embeddings.embed_query, "text")
