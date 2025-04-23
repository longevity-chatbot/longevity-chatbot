from crawler.arxiv_scraper import fetch_papers
from rag.document_store import create_vector_store
from rag.qa_pipeline import generate_answer
from llm.llama_wrapper import load_llama_model

def main():
    print("📚 Fetching papers...")
    papers = fetch_papers("longevity biomarkers", max_results=20)

    print("🧠 Creating vector store...")
    vectorstore = create_vector_store(papers)

    print("🚀 Loading LLaMA model...")
    llama = load_llama_model()

    question = "What are the factors that influence longevity?"
    print(f"\n❓ Question: {question}")
    answer = generate_answer(vectorstore, question, llama)
    print(f"\n💡 Answer: {answer}")

if __name__ == "__main__":
    main()
