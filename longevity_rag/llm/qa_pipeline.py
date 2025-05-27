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
        
        # Create a basic citation
        citation = f"[{i}] {title} - {url}"
        citations.append(citation)

    context = "\n\n".join(context_parts)
    return context, citations
 