
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

def create_vector_store(papers):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    docs = [Document(page_content=p["summary"], metadata={"title": p["title"]}) for p in papers]
    vectorstore = Chroma.from_documents(docs, embedding=embeddings)
    return vectorstore
