import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
import UserProfileModal from './components/UserProfileModal';
import './App.css';

function App() {
  const [currentChat, setCurrentChat] = useState(() => {
    return localStorage.getItem('currentChat') || 'Chat 1';
  });
  const [chats, setChats] = useState(() => {
    const saved = localStorage.getItem('chats');
    return saved ? JSON.parse(saved) : { 'Chat 1': [] };
  });
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });
  const [citationSidebarOpen, setCitationSidebarOpen] = useState(false);
  const [highlightedMessageIndex, setHighlightedMessageIndex] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showProfileModal, setShowProfileModal] = useState(() => {
    return !localStorage.getItem('userProfile');
  });
  const [userProfile, setUserProfile] = useState(() => {
    const saved = localStorage.getItem('userProfile');
    return saved ? JSON.parse(saved) : null;
  });
  const [userId] = useState(() => {
    let id = localStorage.getItem('userId');
    if (!id) {
      id = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('userId', id);
    }
    return id;
  });

  const getAllCitations = () => {
    const allCitations = [];
    chats[currentChat].forEach(message => {
      if (message.citations && message.citations.length > 0) {
        message.citations.forEach(citation => {
          if (!allCitations.find(c => c.url === citation.url)) {
            allCitations.push(citation);
          }
        });
      }
    });
    return allCitations;
  };

  const addNewChat = () => {
    const chatName = `Chat ${Object.keys(chats).length + 1}`;
    setChats(prev => ({ ...prev, [chatName]: [] }));
    setCurrentChat(chatName);
    setHighlightedMessageIndex(null);
  };

  const handleSetCurrentChat = (chatName) => {
    setCurrentChat(chatName);
    // Only clear highlight if switching chats manually (not from search)
    if (highlightedMessageIndex === null) {
      setHighlightedMessageIndex(null);
    }
  };

  const handleSetCurrentChatFromSearch = (chatName, messageIndex, term) => {
    setCurrentChat(chatName);
    setHighlightedMessageIndex(messageIndex);
    setSearchTerm(term);
  };

  const updateCurrentChat = (messages) => {
    setChats(prev => ({ ...prev, [currentChat]: messages }));
    // Auto-save to database
    saveChatToDatabase(currentChat, messages);
    // Clear highlight when messages change
    setHighlightedMessageIndex(null);
    setSearchTerm('');
  };

  const saveChatToDatabase = async (sessionName, messages) => {
    try {
      await fetch('http://localhost:8000/api/save-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_name: `${userId}_${sessionName}`,
          messages: messages,
          user_profile: userProfile
        })
      });
    } catch (error) {
      console.error('Failed to save chat:', error);
    }
  };

  const handleProfileSubmit = async (profile) => {
    const profileWithId = { ...profile, user_id: userId };
    setUserProfile(profileWithId);
    setShowProfileModal(false);
    
    // Save to localStorage
    localStorage.setItem('userProfile', JSON.stringify(profileWithId));
    
    // Save profile to database
    try {
      await fetch('http://localhost:8000/api/save-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_name: `${userId}_${currentChat}`,
          user_profile: profileWithId
        })
      });
    } catch (error) {
      console.error('Failed to save profile:', error);
    }
  };

  const autoRenameChat = (messages) => {
    // Auto-rename chat based on first user message (only after bot responds)
    if (messages.length === 2 && currentChat.startsWith('Chat ')) {
      const firstUserMessage = messages.find(msg => msg.role === 'user');
      if (firstUserMessage) {
        const autoName = firstUserMessage.content.slice(0, 30) + (firstUserMessage.content.length > 30 ? '...' : '');
        // Use setTimeout to ensure state updates don't conflict
        setTimeout(() => {
          renameChat(currentChat, autoName);
        }, 100);
      }
    }
  };

  const deleteChat = (chatName) => {
    if (Object.keys(chats).length === 1) return; // Don't delete last chat
    
    const newChats = { ...chats };
    delete newChats[chatName];
    setChats(newChats);
    
    // Switch to first available chat
    if (currentChat === chatName) {
      setCurrentChat(Object.keys(newChats)[0]);
    }
  };

  const renameChat = (oldName, newName) => {
    if (oldName === newName || chats[newName]) return;
    
    setChats(prev => {
      const newChats = { ...prev };
      newChats[newName] = newChats[oldName];
      delete newChats[oldName];
      return newChats;
    });
    
    if (currentChat === oldName) {
      setCurrentChat(newName);
    }
  };

  // Save to localStorage whenever chats or currentChat changes
  useEffect(() => {
    localStorage.setItem('chats', JSON.stringify(chats));
  }, [chats]);

  useEffect(() => {
    localStorage.setItem('currentChat', currentChat);
  }, [currentChat]);

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
    document.body.className = darkMode ? 'dark-mode' : 'light-mode';
  }, [darkMode]);

  return (
    <div className={`app ${darkMode ? 'dark' : 'light'}`}>
      <UserProfileModal 
        isOpen={showProfileModal}
        onSubmit={handleProfileSubmit}
        onClose={() => setShowProfileModal(false)}
      />
      <Sidebar 
        chats={chats}
        currentChat={currentChat}
        setCurrentChat={handleSetCurrentChat}
        addNewChat={addNewChat}
        deleteChat={deleteChat}
        renameChat={renameChat}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        setCurrentChatFromSearch={handleSetCurrentChatFromSearch}
      />
      <ChatInterface 
        messages={chats[currentChat]}
        updateMessages={updateCurrentChat}
        autoRenameChat={autoRenameChat}
        citationSidebarOpen={citationSidebarOpen}
        setCitationSidebarOpen={setCitationSidebarOpen}
        highlightedMessageIndex={highlightedMessageIndex}
        searchTerm={searchTerm}
      />
      {citationSidebarOpen && (
        <div className="citation-sidebar">
          <div className="citation-sidebar-header">
            <h3>Citations</h3>
            <button 
              className="close-citation-btn"
              onClick={() => setCitationSidebarOpen(false)}
            >
              ×
            </button>
          </div>
          <div className="citation-list">
            {getAllCitations().map((citation, index) => (
              <div key={index} className="citation-sidebar-item">
                <div className="citation-number">[{index + 1}]</div>
                <div className="citation-content">
                  <a 
                    href={citation.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="citation-sidebar-link"
                  >
                    {citation.apa_format || citation.title}
                  </a>
                </div>
              </div>
            ))}
            {getAllCitations().length === 0 && (
              <div className="no-citations">No citations available</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;