import React, { useState } from 'react';

const ChatInterface = ({ messages, updateMessages }) => {
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

      updateMessages([...newMessages, assistantMessage]);
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
      <div className="chat-header">
        <h1>Longevity Research Assistant</h1>
      </div>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div>{message.content}</div>
            {message.citations && message.citations.length > 0 && (
              <div className="citations">
                <strong>Citations:</strong>
                {message.citations.map((citation, i) => (
                  <div key={i}>{citation}</div>
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