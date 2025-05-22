import os 
from crawler.arxiv_scraper import fetch_papers, check_peer_validity
from rag.document_store import create_vector_store
from rag.qa_pipeline import generate_context
from llm.gpt_wrapper import ask_with_relevant_context

def main():
    print("📚 Fetching papers...")
    papers = fetch_papers("longevity biomarkers", max_results=10)

    print(f"🔎 Total fetched: {len(papers)}")

    valid_papers = []
    for i, paper in enumerate(papers, 1):
        print(f"\n🔍 Checking paper {i}: {paper['title'][:80]}...")
        validity = check_peer_validity(paper, verbose=True)  # Enable verbose logging

        if validity["valid"]:
            print(f"✅ VALID — Venue: {validity['venue']}, Citations: {validity['citationCount']}")
            paper.update(validity)  # Optional: attach metadata
            valid_papers.append(paper)
        else:
            print(f"❌ INVALID — Reason: {validity['reason']}")

    print(f"\n📊 Valid papers found: {len(valid_papers)}")

    if not valid_papers:
        print("🚫 No valid papers found. Exiting.")
        return

    print("🧠 Creating vector store...")
    vectorstore = create_vector_store(valid_papers)

    question = "What are the factors that increase lifespan?"
    print(f"\n❓ Question: {question}")
    
    print("🤖 Calling Chat Gpt 3.5 model...")
    answer = ask_with_relevant_context(question, vectorstore)

    print(f"\n💡 Answer: {answer}")


if __name__ == "__main__":
    main()
