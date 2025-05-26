import os
from openai import OpenAI

client = OpenAI(api_key="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")

# Prompt LLM 
def ask_with_context(question, papers, history = None):
    
    history = history or []
    
    context = "\n\n".join(f"{p.metadata.get('title', 'Unknown Title')}:\n{p.page_content}" for p in papers)


    # Add system-level prompt
    messages = [
        {"role": "system", "content": (
            "You are a helpful and knowledgeable scientific assistant specialized in longevity, "
            "cellular aging, and motility. Use the following context to answer the user's questions. "
            "If the user follows up, base your answer on both the context and earlier conversation."
            "Always mention the paper title and publisher."
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