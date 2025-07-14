import streamlit as st
import sys
import os

# Add the longevity_rag directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'longevity_rag'))

from crawler.pubmed_scraper import fetch_pubmed_papers
from rag.document_store import create_vector_store
from llm.gpt_wrapper import ask_with_relevant_context
from utils.keyword_extractor import extract_keywords
from cache.session_cache import SessionCache

# Page config
st.set_page_config(page_title="Longevity Chatbot", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Current Chat": []}
if "session_cache" not in st.session_state:
    st.session_state.session_cache = SessionCache()

# Sidebar for chat history
with st.sidebar:
    st.title("Chat History")
    
    # New chat button
    if st.button("+ New Chat"):
        chat_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[chat_name] = []
        st.session_state.messages = []
        st.session_state.session_cache = SessionCache()  # Reset cache for new chat
    
    # Display chat sessions
    for chat_name in st.session_state.chat_sessions:
        if st.button(chat_name, key=chat_name):
            st.session_state.messages = st.session_state.chat_sessions[chat_name]

# Main chat interface
st.title("🧬 Longevity Research Chatbot")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "citations" in message:
            with st.expander("📚 Citations"):
                for citation in message["citations"]:
                    st.write(citation)

# Chat input
if prompt := st.chat_input("Ask about longevity research..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process with RAG pipeline
    with st.chat_message("assistant"):
        with st.spinner("Searching research papers..."):
            try:
                # Extract keywords and check cache
                keywords = extract_keywords(prompt)
                query_keywords = " ".join(keywords) if keywords else prompt
                
                session_cache = st.session_state.session_cache
                
                if session_cache.has_vectorstore() and session_cache.is_similar_query(query_keywords):
                    st.info("Using cached research papers")
                    vectorstore = session_cache.vectorstore
                else:
                    st.info("Fetching new research papers...")
                    papers = fetch_pubmed_papers(query_keywords, max_results=10)
                    vectorstore = create_vector_store(papers)
                    session_cache.set_vectorstore(vectorstore, query_keywords)
                
                # Get answer
                answer, citations = ask_with_relevant_context(prompt, vectorstore)
                st.markdown(answer)
                
                # Show citations
                if citations:
                    with st.expander("📚 Citations"):
                        for citation in citations:
                            st.write(citation)
                            
            except Exception as e:
                answer = f"Sorry, I encountered an error: {str(e)}"
                citations = []
                st.error(answer)
    
    # Save response
    response_data = {"role": "assistant", "content": answer}
    if citations:
        response_data["citations"] = citations
    st.session_state.messages.append(response_data)
    
    # Save to current session
    current_session = list(st.session_state.chat_sessions.keys())[0]
    st.session_state.chat_sessions[current_session] = st.session_state.messages