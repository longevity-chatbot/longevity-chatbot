import feedparser
import urllib.parse
import requests
import os
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

# Configuration 

client = OpenAI(api_key="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")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create output folder
os.makedirs("arxiv_pdfs", exist_ok=True)

def search_arxiv(query="longevity biology", max_results=5):
    base_url = "http://export.arxiv.org/api/query"
    encoded_query = urllib.parse.quote(query)
    query_url = f"{base_url}?search_query=all:{encoded_query}&start=0&max_results={max_results}"

    feed = feedparser.parse(query_url)
    
    papers = []
    
    for entry in feed.entries:
        pdf_url = entry.id.replace("abs", "pdf") + ".pdf"
        papers.append({
            "title": entry.title,
            "summary": entry.summary,
            "pdf_url": pdf_url,
            "published": entry.published
        })
        
    return papers

def search_europe_pmc(query="longevity biology", limit = 10):
    base_url="https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": query,
        "format": "json",
        "pageSize": limit,
        "resultType": "core"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    results = response.json()["resultList"]["result"]
    
    papers = []
    
    for entry in results:
        papers.append({
            "title": entry.get("title", ""),
            "summary": entry.get("abstractText", ""),
            "source":"EuropePMC",
            "published": entry.get("pubYear", ""),
            "doi": entry.get("doi", ""),
            "fullTextUrl": entry.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url", "")
        })
        
    return papers

# Add emebedding
def embed_abstracts(papers):
    abstracts = [p['summary'] for p in papers]
    embeddings = model.encode(abstracts)
    return embeddings

# Similarity Search
def retrieve_top_k(user_question, papers, embeddings, k=3):
    query_embedding = model.encode([user_question])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:k]
    return [papers[i] for i in top_indices]

# Prompt LLM 
def ask_with_context(question, papers):
    context = "\n\n".join(f"{p['title']}:\n{p['summary']}" for p in papers)
    prompt = f"""Use the following scientific abstracts to answer the question:

{context}

Q: {question}
A:"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or gpt-4
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Full Pipeline
def answer_question_live(question):
    print(f"🔍 Searching arXiv for: {question}")
    arxiv_papers = search_arxiv(question, max_results=10)
    pmc_papers = search_europe_pmc(question, limit=10)
    
    all_papers = arxiv_papers + pmc_papers
    all_papers = [p for p in all_papers if p.get("summary")] #filter out empty abstracts
    
    if not all_papers:
        return "No relevant papers found."

    print(f"📄 Found {len(all_papers)} papers. Embedding...")
    embeddings = embed_abstracts(all_papers)
    top_papers = retrieve_top_k(question, all_papers, embeddings, k=3)

    print(f"✍️ Generating answer using top {len(top_papers)} papers...")
    return ask_with_context(question, top_papers)

# CLI
if __name__ == "__main__":
    question = input("Ask a longevity-related question:\n> ")
    answer = answer_question_live(question)
    print("\n🧠 Answer:\n", answer)