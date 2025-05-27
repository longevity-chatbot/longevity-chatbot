from retrievers.arxiv_retriever import search_arxiv
from retrievers.europepmc_retriever import search_europe_pmc
from embedder import embed_abstracts
from ranker import retrieve_top_k
from responder import ask_with_context

# Full Pipeline
def answer_question_live(question, chat_history):
    print(f"🔍 Searching for: {question}")
    arxiv_docs= search_arxiv(question, max_results=10)
    pmc_docs = search_europe_pmc(question, limit=10)
    
    all_docs = arxiv_docs + pmc_docs
    all_docs = [doc for doc in all_docs if doc.page_content.strip()] #filter out empty abstracts
    
    if not all_docs:
        return "No relevant papers found.", chat_history, []

    print(f"📄 Found {len(all_docs)} papers. Embedding...")
    embeddings = embed_abstracts(all_docs)
    top_papers = retrieve_top_k(question, all_docs, embeddings, k=3)

    print(f"✍️ Generating answer using top {len(top_papers)} papers...")
    answer, chat_history = ask_with_context(question, top_papers, chat_history)
    
    return answer, chat_history, top_papers

# CLI
if __name__ == "__main__":
    question = print("🧬 Longevity Chatbot — Start your chat (type 'exit' to quit)\n")
    chat_history = []
    
    while True:
        question = input("> ")
        if question.lower() in {"exit", "quit"}:
            print("Goodbye!👋🏻")
            break 
        try: 
            answer, chat_history, top_papers = answer_question_live(question, chat_history)
            print("\n🧠 Answer:\n", answer, "\n")
        except Exception as e:
            print(f"⚠️ Error: {e}\n")