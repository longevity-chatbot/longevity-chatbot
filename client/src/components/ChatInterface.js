import React, { useState } from 'react';

const ChatInterface = ({ messages, updateMessages, autoRenameChat, citationSidebarOpen, setCitationSidebarOpen, highlightedMessageIndex, searchTerm }) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [editingIndex, setEditingIndex] = useState(null);
  const [editText, setEditText] = useState('');
  const messagesEndRef = React.useRef(null);
  const highlightedRef = React.useRef(null);

  const sendMessage = async (messageText = input, isEdit = false, editIndex = null) => {
    if (!messageText.trim() || loading) return;

    let newMessages;
    if (isEdit && editIndex !== null) {
      // Remove messages from edit point onwards
      newMessages = messages.slice(0, editIndex);
      newMessages.push({ role: 'user', content: messageText });
    } else {
      const userMessage = { role: 'user', content: messageText };
      newMessages = [...messages, userMessage];
    }
    
    updateMessages(newMessages);
    if (!isEdit) setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: messageText })
      });

      const data = await response.json();
      
      const assistantMessage = {
        role: 'assistant',
        content: data.answer,
        citations: data.citations || []
      };

      const finalMessages = [...newMessages, assistantMessage];
      updateMessages(finalMessages);
      
      // Auto-rename after successful response
      if (autoRenameChat) {
        autoRenameChat(finalMessages);
      }
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        citations: []
      };
      updateMessages([...newMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (index) => {
    setEditingIndex(index);
    setEditText(messages[index].content);
  };

  const saveEdit = () => {
    sendMessage(editText, true, editingIndex);
    setEditingIndex(null);
    setEditText('');
  };

  const cancelEdit = () => {
    setEditingIndex(null);
    setEditText('');
  };

  // Scroll to highlighted message when it changes
  React.useEffect(() => {
    if (highlightedMessageIndex !== null && highlightedRef.current) {
      // Add delay to ensure DOM is updated after chat switch
      setTimeout(() => {
        if (highlightedRef.current) {
          highlightedRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    }
  }, [highlightedMessageIndex, messages]);

  // Auto-scroll to bottom for new messages
  React.useEffect(() => {
    if (highlightedMessageIndex === null) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages.length, highlightedMessageIndex]);

  const highlightText = (text, term) => {
    if (!term || !text) return text;
    
    const regex = new RegExp(`(${term})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? 
        <mark key={index} className="search-highlight">{part}</mark> : 
        part
    );
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div></div>
        <button 
          className={`citation-toggle-btn ${citationSidebarOpen ? 'hidden' : ''}`}
          onClick={() => setCitationSidebarOpen(!citationSidebarOpen)}
          title="Toggle citations"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14,2 14,8 20,8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10,9 9,9 8,9"></polyline>
          </svg>
          Citations
        </button>
      </div>
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div 
            key={index} 
            ref={index === highlightedMessageIndex ? highlightedRef : null}
            className={`message ${message.role} ${index === highlightedMessageIndex ? 'highlighted' : ''}`}
          >
            {editingIndex === index ? (
              <div className="edit-container">
                <textarea
                  value={editText}
                  onChange={(e) => setEditText(e.target.value)}
                  className="edit-textarea"
                  rows={3}
                />
                <div className="edit-buttons">
                  <button onClick={saveEdit} className="save-btn">Save</button>
                  <button onClick={cancelEdit} className="cancel-btn">Cancel</button>
                </div>
              </div>
            ) : (
              <div className="message-content">
                <div>{highlightText(message.content, searchTerm)}</div>
                <div className="message-actions">
                  {message.role === 'user' && (
                    <button 
                      className="edit-btn"
                      onClick={() => handleEdit(index)}
                      title="Edit message"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </button>
                  )}
                  {message.role === 'assistant' && (
                    <button 
                      className="copy-btn"
                      onClick={() => {
                        navigator.clipboard.writeText(message.content);
                      }}
                      title="Copy message"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                      </svg>
                    </button>
                  )}
                </div>
              </div>
            )}
            {message.citations && message.citations.length > 0 && (
              <div className="citations">
                <strong>Citations:</strong>
                {message.citations.map((citation, i) => (
                  <div key={i} className="citation-item">
                    <a 
                      href={citation.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="citation-link"
                    >
                      {citation.apa_format || `[${citation.id}] ${citation.title}`}
                    </a>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="message assistant loading">Searching research papers...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about longevity research..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading || !input.trim()}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;