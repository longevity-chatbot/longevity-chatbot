"""
def generate_context(vectorstore, query):
    #performs a similarity search in the vectorstore to find the top 3 documents that are most similar to a given query.
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    return context
"""
def generate_context(vectorstore, query):
    # Get top-k similar documents
    docs = vectorstore.similarity_search(query, k=3)
    
    # Build context string and keep references
    context_parts = []
    citations = []
    
    for i, doc in enumerate(docs, start=1):
        content = doc.page_content.strip()
        title = doc.metadata.get("title", "Unknown Title")
        url = doc.metadata.get("url", "No URL")

        # Add summary to the context
        context_parts.append(f"[{i}] {content}")
        
        # Generate proper APA 7 citation
        from datetime import datetime
        
        # Get authors from metadata (now stored as comma-separated string)
        authors_str = doc.metadata.get("authors", "")
        
        # Format authors for APA style
        if authors_str:
            authors = [a.strip() for a in authors_str.split(",")]
            if len(authors) == 1:
                author_text = authors[0]
            elif len(authors) <= 2:
                author_text = " & ".join(authors)
            else:
                author_text = f"{authors[0]} et al."
        else:
            author_text = "Unknown Author"
        
        # Get publication year from metadata or use current year
        year = doc.metadata.get("year", str(datetime.now().year))
        
        # APA 7 format: Author, A. A. (Year). Title. PubMed. Retrieved from URL
        apa_citation = f"{author_text} ({year}). {title}. PubMed. Retrieved from {url}"
        
        citation = {
            "id": i,
            "title": title,
            "url": url,
            "apa_format": apa_citation
        }
        citations.append(citation)

    context = "\n\n".join(context_parts)
    return context, citations
 