# 🧬 Longevity QA Chatbot using RAG, arXiv & Semantic Scholar

This project is an intelligent chatbot for answering questions related to **longevity, biomarkers, and biomedical research**. It combines a **Retrieval-Augmented Generation (RAG)** approach using:

- Scientific literature scraped from **arXiv**
- Peer-reviewed validation via **Semantic Scholar**
- Embedding-based document retrieval using **HuggingFace Transformers + Chroma**
- Answer generation using **OpenAI GPT-3.5**

---

## 🚀 Features

- 🔍 **Web crawler** for fetching scientific abstracts from arXiv based on user-defined queries
- ✅ **Peer validity checking** using Semantic Scholar API (e.g., citation count, venue)
- 🧠 **Vector store and similarity search** for contextual document retrieval
- 🤖 **Chatbot integration** using OpenAI's GPT-3.5 to answer scientific questions

---

## 🛠️ How It Works

1. **Fetch Papers**: 
   - Uses `fetch_papers()` to scrape abstracts from arXiv based on a keyword like `"longevity biomarkers"`.

2. **Validate Papers**: 
   - Calls `check_peer_validity()` to ensure the paper is credible using Semantic Scholar (based on citation count and journal).

3. **Create Embeddings**:
   - Generates vector embeddings using HuggingFace's `all-MiniLM-L6-v2` model and stores them in Chroma.

4. **Query and Contextualize**:
   - Uses `generate_context()` to retrieve the top-k most relevant papers for a given user query.

5. **Answer Generation**:
   - Sends the query and context to OpenAI's GPT-3.5 to generate a natural language response.

---

## 📦 Project Structure

```
.
├── main.py                      # Entry point of the application
├── crawler/
│   └── arxiv_scraper.py        # Fetches and validates papers
├── rag/
│   ├── document_store.py       # Creates vector store
│   └── qa_pipeline.py          # Generates context using similarity search
├── llm/
│   └── gpt_wrapper.py          # Calls OpenAI API with context
├── README.md                   # You're here!
```

---

## 🧪 Example

```bash
📚 Fetching papers...
🔍 Checking paper 1: Economic impact of biomarker-based aging interventions...
✅ VALID — Venue: Nature Aging, Citations: 152

🧠 Creating vector store...

❓ Question: What are the factors that increase lifespan?
🤖 Calling Chat Gpt 3.5 model...

💡 Answer: Lifestyle factors such as diet, exercise, and stress reduction, along with genetic and biomarker-related interventions, contribute significantly to increased lifespan...
```

---

## 🔐 Requirements

- Python 3.8+
- OpenAI API Key (for GPT-3.5)
- Semantic Scholar API Key (recommended)
- HuggingFace Transformers
- LangChain
- Chroma or FAISS

Install dependencies:

```bash
pip install openai requests langchain chromadb huggingface-hub
```

---

## 📚 APIs Used

- [OpenAI API](https://platform.openai.com/)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [arXiv API](https://arxiv.org/help/api/index)

---

## 🧠 Future Improvements

- Use full PDFs from arXiv for deeper context
- Add GUI or chatbot interface
- Store vectorstore persistently (e.g., ChromaDB with local DB)
- Multi-turn chat memory

---

## 📜 License

MIT License — feel free to use, modify, and share with attribution.

---

## 👨‍🔬 Author

Designed for research and educational use in the domain of **longevity and biomedical AI**.
