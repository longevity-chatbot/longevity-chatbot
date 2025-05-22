from retrievers.arxiv_retriever import search_arxiv
from retrievers.europepmc_retriever import search_europe_pmc
from embedder import embed_abstracts
from ranker import retrieve_top_k
from responder import ask_with_context

# Full Pipeline
def answer_question_live(question):
    print(f"🔍 Searching arXiv for: {question}")
    arxiv_docs= search_arxiv(question, max_results=10)
    pmc_docs = search_europe_pmc(question, limit=10)
    
    all_docs = arxiv_docs + pmc_docs
    all_docs = [doc for doc in all_docs if doc.page_content.strip()] #filter out empty abstracts
    
    if not all_docs:
        return "No relevant papers found."

    print(f"📄 Found {len(all_docs)} papers. Embedding...")
    embeddings = embed_abstracts(all_docs)
    top_papers = retrieve_top_k(question, all_docs, embeddings, k=3)

    print(f"✍️ Generating answer using top {len(top_papers)} papers...")
    return ask_with_context(question, top_papers)

# CLI
if __name__ == "__main__":
    question = input("Ask a longevity-related question:\n> ")
    answer = answer_question_live(question)
    print("\n🧠 Answer:\n", answer)