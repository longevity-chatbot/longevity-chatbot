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

        keywords = extract_keywords(question)
        query_keywords = " ".join(keywords) if keywords else question

        # Check if we can reuse the cached vectorstore
        if session_cache.has_vectorstore() and session_cache.is_similar_query(query_keywords):
            print("🗂️ Using session-cached vectorstore.")
            vectorstore = session_cache.vectorstore
        else:
            print("📚 Fetching papers from PubMed...")
            papers = fetch_pubmed_papers(query_keywords, max_results=10)
            print("🧠 Creating vector store...")
            vectorstore = create_vector_store(papers)
            session_cache.set_vectorstore(vectorstore, query_keywords)

        print(f"\n❓ Question: {question}")
        print("🤖 Calling OpenAI model...")
        answer, citations = ask_with_relevant_context(question, vectorstore)
        print(f"\n💡 Answer: {answer}  \n✅ and Citations: {citations}")

if __name__ == "__main__":
    main()
