
def generate_context(vectorstore, query):
    #performs a similarity search in the vectorstore to find the top 3 documents that are most similar to a given query.
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    return context
