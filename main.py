from retrievers.arxiv_retriever import search_arxiv
from retrievers.europepmc_retriever import search_europe_pmc
from embedder import embed_abstracts
from ranker import retrieve_top_k
from responder import ask_with_context

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