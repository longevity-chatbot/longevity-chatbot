import sqlite3
import json
from datetime import datetime

class ChatDatabase:
    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            # Drop existing tables if they exist
            conn.execute("DROP TABLE IF EXISTS messages")
            conn.execute("DROP TABLE IF EXISTS chat_sessions")
            
            # Create fresh tables
            conn.execute("""
                CREATE TABLE chat_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    citations TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def save_chat_session(self, session_name: str, messages: list):
        with sqlite3.connect(self.db_path) as conn:
            # Insert or update session
            conn.execute(
                "INSERT OR REPLACE INTO chat_sessions (session_name, updated_at) VALUES (?, ?)",
                (session_name, datetime.now())
            )
            
            # Clear existing messages for this session
            conn.execute("DELETE FROM messages WHERE session_name = ?", (session_name,))
            
            # Insert messages
            for msg in messages:
                citations_json = json.dumps(msg.get('citations', []))
                conn.execute(
                    "INSERT INTO messages (session_name, role, content, citations) VALUES (?, ?, ?, ?)",
                    (session_name, msg['role'], msg['content'], citations_json)
                )
    
    def get_chat_session(self, session_name: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT role, content, citations FROM messages WHERE session_name = ? ORDER BY id",
                (session_name,)
            )
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'role': row[0],
                    'content': row[1],
                    'citations': json.loads(row[2]) if row[2] else []
                })
            return messages
    
    def get_all_sessions(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT session_name FROM chat_sessions ORDER BY updated_at DESC")
            return [row[0] for row in cursor.fetchall()]