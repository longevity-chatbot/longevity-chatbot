import React, { useState } from 'react';

const Sidebar = ({ chats, currentChat, setCurrentChat, addNewChat, deleteChat, renameChat, darkMode, setDarkMode }) => {
  const [editingChat, setEditingChat] = useState(null);
  const [newName, setNewName] = useState('');

  const handleRename = (oldName) => {
    if (newName.trim() && newName !== oldName) {
      renameChat(oldName, newName.trim());
    }
    setEditingChat(null);
    setNewName('');
  };
  return (
    <div className="sidebar">
      <h2>🧬 Longevity Chat</h2>
      <button className="new-chat-btn" onClick={addNewChat}>
        + New Chat
      </button>
      <div className="chat-list">
        {Object.keys(chats).map(chatName => (
          <div key={chatName} className={`chat-item ${chatName === currentChat ? 'active' : ''}`}>
            {editingChat === chatName ? (
              <input
                className="chat-rename-input"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                onBlur={() => handleRename(chatName)}
                onKeyPress={(e) => e.key === 'Enter' && handleRename(chatName)}
                autoFocus
              />
            ) : (
              <div className="chat-name-container">
                <div 
                  className="chat-name" 
                  onClick={() => setCurrentChat(chatName)}
                  onDoubleClick={() => {
                    setEditingChat(chatName);
                    setNewName(chatName);
                  }}
                  title="Double-click to rename"
                >
                  {chatName}
                </div>
                <button 
                  className="rename-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    setEditingChat(chatName);
                    setNewName(chatName);
                  }}
                  title="Rename chat"
                >
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
              </div>
            )}
            {Object.keys(chats).length > 1 && (
              <button 
                className="delete-chat-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteChat(chatName);
                }}
              >
                ×
              </button>
            )}
          </div>
        ))}
      </div>
      <button 
        className="theme-toggle-bottom"
        onClick={() => setDarkMode(!darkMode)}
        title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          {darkMode ? (
            <circle cx="12" cy="12" r="5"></circle>
          ) : (
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          )}
        </svg>
      </button>
    </div>
  );
};

export default Sidebar;