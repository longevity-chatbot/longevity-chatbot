import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
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

  const addNewChat = () => {
    const chatName = `Chat ${Object.keys(chats).length + 1}`;
    setChats(prev => ({ ...prev, [chatName]: [] }));
    setCurrentChat(chatName);
  };

  const updateCurrentChat = (messages) => {
    setChats(prev => ({ ...prev, [currentChat]: messages }));
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
      <Sidebar 
        chats={chats}
        currentChat={currentChat}
        setCurrentChat={setCurrentChat}
        addNewChat={addNewChat}
        deleteChat={deleteChat}
        renameChat={renameChat}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
      />
      <ChatInterface 
        messages={chats[currentChat]}
        updateMessages={updateCurrentChat}
        autoRenameChat={autoRenameChat}
      />
    </div>
  );
}

export default App;