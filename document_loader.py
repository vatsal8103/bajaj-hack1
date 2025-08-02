import requests
from io import BytesIO
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)

def load_document(doc_url):
    ext = doc_url.split('.')[-1].lower().split('?')[0]
    file_data = download_file(doc_url)
    if ext == "pdf":
        loader = PyPDFLoader(file_data)
        docs = loader.load()
    elif ext in ("docx", "doc"):
        loader = Docx2txtLoader(file_data)
        docs = loader.load()
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return docs
