import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
import './App.css';

function App() {
  const [currentChat, setCurrentChat] = useState('Chat 1');
  const [chats, setChats] = useState({
    'Chat 1': []
  });

  const addNewChat = () => {
    const chatName = `Chat ${Object.keys(chats).length + 1}`;
    setChats(prev => ({ ...prev, [chatName]: [] }));
    setCurrentChat(chatName);
  };

  const updateCurrentChat = (messages) => {
    setChats(prev => ({ ...prev, [currentChat]: messages }));
  };

  return (
    <div className="app">
      <Sidebar 
        chats={chats}
        currentChat={currentChat}
        setCurrentChat={setCurrentChat}
        addNewChat={addNewChat}
      />
      <ChatInterface 
        messages={chats[currentChat]}
        updateMessages={updateCurrentChat}
      />
    </div>
  );
}

export default App;