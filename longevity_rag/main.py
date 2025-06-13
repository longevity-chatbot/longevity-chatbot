import os 
from crawler.arxiv_scraper import fetch_papers
from rag.document_store import create_vector_store
from llm.gpt_wrapper import ask_with_relevant_context
from crawler.arxiv_scraper import check_peer_validity

def main():

    question = "How many hours should I do intermmittent fasting?"

    print("📚 Fetching papers...")
    papers = fetch_papers(question, max_results=5)

    print(f"🔎 Total fetched: {len(papers)}")
  
    valid_papers = []
    for i, paper in enumerate(papers, 1):
        print(f"\n🔍 Checking paper {i}: {paper['title'][:80]}...")
        validity = check_peer_validity(paper, verbose=True)  # Enable verbose logging

        if validity["valid"]:
            print(f"✅ VALID — Venue: {validity['journal']}")
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

    
    print(f"\n❓ Question: {question}")
    
    print("🤖 Calling Chat Gpt 3.5 model...")
    answer, citations = ask_with_relevant_context(question, vectorstore)

    print(f"\n💡 Answer: {answer}  \n✅ and Citations: {citations}")


if __name__ == "__main__":
    main()
