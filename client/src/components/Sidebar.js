import React, { useState, useEffect, useRef } from 'react';

const Sidebar = ({ chats, currentChat, setCurrentChat, addNewChat, deleteChat, renameChat, darkMode, setDarkMode, setCurrentChatFromSearch, exportCurrentChat }) => {
  const [editingChat, setEditingChat] = useState(null);
  const [newName, setNewName] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showSearch, setShowSearch] = useState(false);
  const [showExportDropdown, setShowExportDropdown] = useState(false);
  const searchRef = useRef(null);
  const exportRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSearch(false);
        setSearchQuery('');
        setSearchResults([]);
      }
      if (exportRef.current && !exportRef.current.contains(event.target)) {
        setShowExportDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const searchChats = (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }
    
    const results = [];
    Object.entries(chats).forEach(([chatName, messages]) => {
      messages.forEach((message, index) => {
        if (message.content.toLowerCase().includes(query.toLowerCase())) {
          results.push({
            chatName,
            messageIndex: index,
            content: message.content,
            role: message.role
          });
        }
      });
    });
    setSearchResults(results);
  };

  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    searchChats(query);
  };

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
      <div className="search-container" ref={searchRef}>
        <button 
          className="search-toggle-btn"
          onClick={() => setShowSearch(!showSearch)}
          title="Search conversations"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
        </button>
        {showSearch && (
          <input
            type="text"
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={handleSearch}
            className="search-input"
            autoFocus
          />
        )}
      </div>
      {searchQuery && searchResults.length > 0 && (
        <div className="search-results">
          <div className="search-results-header">Search Results ({searchResults.length})</div>
          {searchResults.map((result, index) => (
            <div 
              key={index} 
              className="search-result-item"
              onMouseDown={(e) => {
                e.preventDefault();
                setCurrentChatFromSearch(result.chatName, result.messageIndex, searchQuery);
                setSearchQuery('');
                setSearchResults([]);
                setShowSearch(false);
              }}
            >
              <div className="search-result-chat">{result.chatName}</div>
              <div className="search-result-content">
                {result.content.length > 80 ? result.content.substring(0, 80) + '...' : result.content}
              </div>
            </div>
          ))}
        </div>
      )}
      {searchQuery && searchResults.length === 0 && (
        <div className="no-search-results">No results found</div>
      )}
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
      <div className="export-section" ref={exportRef}>
        <button 
          className="export-main-btn"
          onClick={() => setShowExportDropdown(!showExportDropdown)}
          title="Export current chat"
        >
          📤 Export Chat
        </button>
        {showExportDropdown && (
          <div className="export-dropdown">
            <button 
              className="export-option"
              onClick={() => {
                exportCurrentChat('csv');
                setShowExportDropdown(false);
              }}
            >
              📊 CSV
            </button>
            <button 
              className="export-option"
              onClick={() => {
                exportCurrentChat('json');
                setShowExportDropdown(false);
              }}
            >
              📄 JSON
            </button>
          </div>
        )}
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