import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses INFO and WARNING logs from TensorFlow

import tensorflow as tf
warnings.filterwarnings("ignore", category=FutureWarning)  # Suppresses some future/deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.docstore.document import Document

def create_vector_store(papers):
    #generates embeddings (numerical representations) for each paper's summary using a pre-trained model (all-MiniLM-L6-v2)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #creates a list of Document objects, each containing a paper's summary and title. 
    docs = [Document(page_content=p["summary"], metadata={"title": p["title"], "url": p["url"], "authors": ", ".join(p["authors"]) if p["authors"] else "", "year": p["year"]}) for p in papers]
    # it stores these documents in a vector store (Chroma) for efficient retrieval based on similarity
    vectorstore = Chroma.from_documents(docs, embedding=embeddings)
    return vectorstore
