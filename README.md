# 🧬 Longevity Research Chatbot

An intelligent chatbot that answers questions about **longevity, biomarkers, and biomedical research** using a Retrieval-Augmented Generation (RAG) approach. It fetches scientific papers from PubMed, creates vector embeddings, and generates research-backed answers using OpenAI.

## 🚀 Features

- **Research-backed answers** from PubMed scientific literature
- **Modern React UI** with chat history and citations
- **Smart caching** to avoid redundant API calls
- **FastAPI server** for scalable deployment
- **Multiple interfaces** - React web app, Streamlit, or CLI

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

**Option A: React Web App (Recommended)**
```bash
# Start server
uvicorn server.main:app --reload

# Start client (new terminal)
cd client
npm install
npm start
```
Access at `http://localhost:3000`

**Option B: Streamlit Interface**
```bash
streamlit run streamlit-ui/app.py
```

**Option C: Command Line**
```bash
python longevity_rag/main.py
```

## 📁 Project Structure

- `longevity_rag/` - Core RAG pipeline (Python)
- `server/` - FastAPI backend
- `client/` - React frontend
- `streamlit-ui/` - Alternative Streamlit interface

## 📜 License

MIT License
