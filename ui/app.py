import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="Longevity Chatbot", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"Current Chat": []}

# Sidebar for chat history
with st.sidebar:
    st.title("Chat History")
    
    # New chat button
    if st.button("+ New Chat"):
        chat_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
        st.session_state.chat_sessions[chat_name] = []
        st.session_state.messages = []
    
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

# Chat input
if prompt := st.chat_input("Ask about longevity research..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add assistant response (placeholder)
    with st.chat_message("assistant"):
        response = f"You asked: {prompt}\n\n*This is a placeholder response. Connect your RAG pipeline here.*"
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Save to current session
    current_session = list(st.session_state.chat_sessions.keys())[0]
    st.session_state.chat_sessions[current_session] = st.session_state.messages