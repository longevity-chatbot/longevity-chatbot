# 🧬 Longevity Research Q&A System

This is a local, AI-powered **Question Answering (QA) system** designed to explore scientific literature on **longevity**. It automatically pulls research papers from [arXiv](https://arxiv.org/), embeds them into a vector store, and allows users to ask questions—answered by a locally running LLM.

## 🚀 Features

- 🔎 **Fetches scientific papers** from arXiv based on a query (e.g., "longevity biomarkers")
- 🧠 **Embeds and stores** research content into a vector store for semantic search
- 💬 **Answers questions** using a local large language model (LLM)
- 🛠️ **Fully offline-compatible** once models are downloaded
- 🤖 Uses **LLaMA 2 7B Chat** (`llama-2-7b-chat.Q4_K_M.gguf`) via `llama.cpp` for local inference

## 📦 Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- Download the LLaMA 2 7B Chat model (`.gguf` format) and place it in:
  ```
  longevity_rag/llm/llama-2-7b-chat.Q4_K_M.gguf
  ```

## 📂 Project Structure

```
longevity_rag_project/
│
├── crawler/
│   └── arxiv_scraper.py      # Scrapes arXiv papers using BeautifulSoup
│
├── rag/
│   ├── document_store.py     # Creates the vector store from papers
│   └── qa_pipeline.py        # Generates answers using the vector store + LLM
│
├── llm/
│   ├── llama_wrapper.py      # Loads LLaMA model using llama.cpp
│   └── llama-2-7b-chat.Q4_K_M.gguf  # Place your model here
│
└── main.py                   # Entry point for the QA system
```

## 💡 Example Question

When run, the system fetches recent longevity papers, builds a vector store, and answers:

> **"What are the factors that influence longevity?"**

## 🧠 Model Details

- **Model:** [Meta AI's LLaMA 2 7B Chat](https://ai.meta.com/llama/)
- **Quantization:** `Q4_K_M` (GGUF format)
- **Inference Backend:** [`llama.cpp`](https://github.com/ggerganov/llama.cpp) (Python bindings via `llama-cpp-python`)

## 🏁 Getting Started

```bash
python main.py
```

## 📜 License

This project is for educational and research purposes only. Ensure compliance with [arXiv's Terms of Use](https://arxiv.org/help/general) and [Meta's LLaMA license](https://ai.meta.com/resources/models-and-libraries/llama-downloads/).