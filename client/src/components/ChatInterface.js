import React, { useState } from 'react';

const ChatInterface = ({ messages, updateMessages, autoRenameChat }) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    updateMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input })
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

  return (
    <div className="chat-interface">

      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              <div>{message.content}</div>
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