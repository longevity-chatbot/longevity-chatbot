import os 
from crawler.pubmed_scraper import fetch_pubmed_papers
from rag.document_store import create_vector_store
from llm.gpt_wrapper import ask_with_relevant_context
from utils.keyword_extractor import extract_keywords
from cache.session_cache import SessionCache

def main():
    session_cache = SessionCache()

    while True:
        question = input("❓ Your question: ").strip()
        if not question:
            print("🚫 No question provided. Exiting.")
            break
        
        print(f"📝 Processing question: '{question}'")

        from utils.keyword_extractor import create_longevity_query
        try:
            query_keywords = create_longevity_query(question)
            print(f"🔍 Search query: '{query_keywords}'")
        except Exception as e:
            print(f"❌ Error in query creation: {e}")
            continue

        # Check if we can reuse the cached vectorstore
        if session_cache.has_vectorstore() and session_cache.is_similar_query(query_keywords):
            print("🗂️ Using session-cached vectorstore.")
            vectorstore = session_cache.vectorstore
        else:
            print("📚 Fetching papers from PubMed...")
            try:
                papers = fetch_pubmed_papers(query_keywords, max_results=15)
                print(f"📄 Found {len(papers)} papers with primary search")
            except Exception as e:
                print(f"❌ Error fetching papers: {e}")
                papers = []
            
            if not papers:
                print("❌ No papers found. Trying broader search...")
                # Fallback to simpler query
                fallback_query = " ".join(extract_keywords(question, max_keywords=3))
                print(f"🔍 Fallback query: '{fallback_query}'")
                papers = fetch_pubmed_papers(fallback_query, max_results=15)
                print(f"📄 Found {len(papers)} papers with fallback search")
            
            if not papers:
                print("❌ No relevant papers found for this query.")
                print("💡 Try simpler terms like: 'lifespan healthspan difference' or 'aging biomarkers'")
                continue
            
            # Filter out papers with empty abstracts
            valid_papers = [p for p in papers if p.get("summary", "").strip() and p["summary"] != "No abstract available"]
            print(f"🧠 Creating vector store with {len(valid_papers)} valid papers (filtered from {len(papers)})...")
            
            if not valid_papers:
                print("❌ No papers with valid abstracts found.")
                continue
                
            try:
                vectorstore = create_vector_store(valid_papers)
            except Exception as e:
                print(f"❌ Error creating vector store: {e}")
                continue
            session_cache.set_vectorstore(vectorstore, query_keywords)

        print(f"\n❓ Question: {question}")
        print("🤖 Calling OpenAI model...")
        answer, citations = ask_with_relevant_context(question, vectorstore)
        print(f"\n💡 Answer: {answer}  \n✅ and Citations: {citations}")

if __name__ == "__main__":
    main()
