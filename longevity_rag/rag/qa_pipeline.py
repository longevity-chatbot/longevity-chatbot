
def generate_answer(vectorstore, query, llama_instance):
    docs = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a scientific expert. Use the following context to answer:

    Context: {context}

    Question: {query}

    Answer:"""

    result = llama_instance(prompt, max_tokens=300)
    return result["choices"][0]["text"].strip()
