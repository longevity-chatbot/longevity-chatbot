import os
from openai import OpenAI
from llm.qa_pipeline import generate_context



client = OpenAI(api_key="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")

def truncate(text, max_chars=1000):
    return text[:max_chars] + "..." if len(text) > max_chars else text 

# Prompt LLM 
def ask_with_context(question, papers, history = None):
    
    history = history or []
    
    # Compose formatted context with metadata
    context = "\n\n".join(
        f"Title: {p.metadata.get('title', 'N/A')}\n"
        f"Published: {p.metadata.get('published', 'N/A')}\n"
        f"Source: {p.metadata.get('source', 'N/A')}\n"
        f"DOI: {p.metadata.get('doi', 'N/A')}\n"
        f"{truncate(p.page_content)}"
        for p in papers
    )

    # Add system-level prompt
    messages = [
        {"role": "system", "content": (
            "You are a scientific assistant specializing in longevity, cellular aging, and motility.\n"
            "You must use only the following document context to answer questions. Do not make up facts.\n"
            "If a user asks for information (e.g. publishing date or journal) and it is missing, say so.\n"
            "Answer clearly and concisely. Cite specific papers only if their metadata is included below."
        )}
    ]

    # Add conversation history
    messages.extend(history)

    # Inject the current question with the new context
    user_message = f"Context:\n{context}\n\nQuestion: {question}"
    messages.append({"role": "user", "content": user_message})

    # Ask the model
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # or gpt-3.5-turbo if needed
        messages=messages
    )

    answer = response.choices[0].message.content

    # Update history for next turn
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})

    return answer, history
