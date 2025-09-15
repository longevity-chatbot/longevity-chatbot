from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add longevity_rag to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'longevity_rag'))
# Add server to path
sys.path.append(os.path.dirname(__file__))

from crawler.pubmed_scraper import fetch_pubmed_papers
from rag.document_store import create_vector_store
from llm.gpt_wrapper import ask_with_relevant_context
from utils.keyword_extractor import extract_keywords
from cache.session_cache import SessionCache
from database import ChatDatabase

app = FastAPI(title="Longevity Chatbot API")

# CORS middleware for React client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session cache and database
session_cache = SessionCache()
db = ChatDatabase()

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

@app.post("/api/save-chat")
async def save_chat(data: dict):
    try:
        session_name = data["session_name"]
        messages = data["messages"]
        user_profile = data.get("user_profile")
        db.save_chat_session(session_name, messages, user_profile)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/save-profile")
async def save_profile(data: dict):
    try:
        session_name = data["session_name"]
        user_profile = data["user_profile"]
        db.save_user_profile(session_name, user_profile)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/load-chat/{session_name}")
async def load_chat(session_name: str):
    try:
        messages = db.get_chat_session(session_name)
        return {"messages": messages, "status": "success"}
    except Exception as e:
        return {"messages": [], "status": "error", "message": str(e)}

@app.get("/api/sessions")
async def get_sessions():
    try:
        sessions = db.get_all_sessions()
        return {"sessions": sessions, "status": "success"}
    except Exception as e:
        return {"sessions": [], "status": "error", "message": str(e)}

@app.get("/api/admin/export-all")
async def export_all_chats():
    try:
        sessions = db.get_all_sessions()
        all_data = []
        for session_name in sessions:
            messages = db.get_chat_session(session_name)
            all_data.append({
                "session_name": session_name,
                "messages": messages
            })
        return {"data": all_data, "total_sessions": len(sessions)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)