import React from 'react';

const Sidebar = ({ chats, currentChat, setCurrentChat, addNewChat }) => {
  return (
    <div className="sidebar">
      <h2>🧬 Longevity Chat</h2>
      <button className="new-chat-btn" onClick={addNewChat}>
        + New Chat
      </button>
      <div className="chat-list">
        {Object.keys(chats).map(chatName => (
          <div
            key={chatName}
            className={`chat-item ${chatName === currentChat ? 'active' : ''}`}
            onClick={() => setCurrentChat(chatName)}
          >
            {chatName}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;