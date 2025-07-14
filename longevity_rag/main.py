import os 
from crawler.pubmed_scraper import fetch_pubmed_papers
from rag.document_store import create_vector_store
from llm.gpt_wrapper import ask_with_relevant_context
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

    
    print("📚 Fetching papers from PubMed...")
    papers = fetch_pubmed_papers(query, max_results=10)
    for i, paper in enumerate(papers, start = 1):
        print(f"\n🔍 Checking paper {i}: {paper['title'][:80]}...")

    print("🧠 Creating vector store...")
    vectorstore = create_vector_store(papers)

    
    print(f"\n❓ Question: {question}")
    
    print("🤖 Calling OpenAI model...")
    answer, citations = ask_with_relevant_context(question, vectorstore)

    print(f"\n💡 Answer: {answer}  \n✅ and Citations: {citations}")


if __name__ == "__main__":
    main()
