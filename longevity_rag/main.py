import os 
from crawler.arxiv_scraper import fetch_papers
from crawler.pubmed_scraper import fetch_pubmed_papers
from rag.document_store import create_vector_store
from llm.gpt_wrapper import ask_with_relevant_context
from crawler.arxiv_scraper import check_peer_validity
from utils.keyword_extractor import extract_keywords

def main():

    # Prompt the user for a question
    question = input("❓ Your question: ").strip()
    if not question:
        print("🚫 No question provided. Exiting.")
        return
    
    # Extract keywords to build a concise query
    keywords = extract_keywords(question)
    if keywords:
        query = " ".join(keywords)
        print(f"🔑 Extracted keywords query: {query}")
    else:
        query = question
        print("⚠️ No keywords extracted, using full question as query.")

    print("📚 Fetching papers from ArXiv...")
    arxiv_papers = fetch_papers(query, max_results=3)
    print(f"🔎 ArXiv papers: {len(arxiv_papers)}")
    
    print("📚 Fetching papers from PubMed...")
    pubmed_papers = fetch_pubmed_papers(query, max_results=7)
    print(f"🔎 PubMed papers: {len(pubmed_papers)}")
    
    # Combine all papers
    papers = arxiv_papers + pubmed_papers
    print(f"🔎 Total fetched: {len(papers)}")
  
    valid_papers = []
    for i, paper in enumerate(papers, 1):
        source = paper.get('source', 'ArXiv')
        print(f"\n🔍 Checking paper {i} [{source}]: {paper['title'][:80]}...")
        
        # Skip validation for PubMed papers (already peer-reviewed)
        if source == 'PubMed':
            print(f"✅ VALID — Source: PubMed (peer-reviewed)")
            valid_papers.append(paper)
        else:
            validity = check_peer_validity(paper, verbose=True)
            if validity["valid"]:
                print(f"✅ VALID — Venue: {validity['journal']}")
                paper.update(validity)
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
    
    print("🤖 Calling OpenAI model...")
    answer, citations = ask_with_relevant_context(question, vectorstore)

    print(f"\n💡 Answer: {answer}  \n✅ and Citations: {citations}")


if __name__ == "__main__":
    main()
