from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add longevity_rag to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'longevity_rag'))

from crawler.pubmed_scraper import fetch_pubmed_papers
from rag.document_store import create_vector_store
from llm.gpt_wrapper import ask_with_relevant_context
from utils.keyword_extractor import extract_keywords
from cache.session_cache import SessionCache

app = FastAPI(title="Longevity Chatbot API")

# CORS middleware for React client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session cache
session_cache = SessionCache()

@app.post("/api/chat")
async def chat(message: dict):
    try:
        question = message["question"]
        
        # Extract keywords and check cache
        keywords = extract_keywords(question)
        query_keywords = " ".join(keywords) if keywords else question
        
        if session_cache.has_vectorstore() and session_cache.is_similar_query(query_keywords):
            vectorstore = session_cache.vectorstore
        else:
            papers = fetch_pubmed_papers(query_keywords, max_results=10)
            vectorstore = create_vector_store(papers)
            session_cache.set_vectorstore(vectorstore, query_keywords)
        
        answer, citations = ask_with_relevant_context(question, vectorstore)
        
        return {
            "answer": answer,
            "citations": citations,
            "status": "success"
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "citations": [],
            "status": "error"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)