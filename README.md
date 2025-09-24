# 🧬 Longevity Research Chatbot

An intelligent chatbot that answers questions about **longevity, biomarkers, and biomedical research** using a Retrieval-Augmented Generation (RAG) approach. It fetches scientific papers from PubMed, creates vector embeddings, and generates research-backed answers using OpenAI.

## 🚀 Features

- **Research-backed answers** from PubMed scientific literature
- **Modern React UI** with chat history and citations
- **Smart caching** to avoid redundant API calls
- **FastAPI server** for scalable deployment
- **Multiple interfaces** - React web app or CLI

## 🛠️ Setup

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install spaCy model
python -m spacy download en_core_web_sm
```

### 2. Set Environment Variables
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application

**IMPORTANT: Always run commands from the project root directory (`longevity-chatbot/`)**

**Option A: React Web App (Recommended)**
```bash
# Start server (from project root)
uvicorn server.main:app --reload

# Start client (new terminal, from project root)
cd client
npm install
npm start
```
Access at `http://localhost:3000`

**Option B: Command Line**
```bash
# From project root
python -m server.cli
```

## 📁 Project Structure

```
longevity-chatbot/
├── server/                 # FastAPI backend with RAG pipeline
│   ├── cache/             # Session caching
│   ├── crawler/           # PubMed data fetching
│   ├── llm/              # OpenAI integration & conversation handling
│   ├── rag/              # Vector store & document processing
│   ├── utils/            # Keyword extraction utilities
│   ├── main.py           # FastAPI server
│   ├── cli.py            # Command line interface
│   └── database.py       # Chat history database
├── client/               # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md
```

## 📜 License

MIT License
