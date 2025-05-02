import os
from openai import OpenAI

client = OpenAI(api_key="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")

# Prompt LLM 
def ask_with_context(question, papers):
    context = "\n\n".join(f"{p.metadata.get('title', 'Unknown Title')}:\n{p.page_content}" for p in papers)
    prompt = f"""You are an AI assistant trained in longevity science, cellular aging, motility, and mobility. Your job is to provide accurate, concise, and well-cited answers based on the provided context:

{context}

Instructions:
- Answer the user's question using only the context.
- Include at least one scientific citation (year ≥ 2020) from the context if possible.
- Write in clear, layman-friendly language suitable for educated non-experts.
- If the answer is uncertain, state what is known and what remains unknown.

Q: {question}
A:"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or gpt-4
        messages=[{"role": "user", "content": "You are a helpful scientific assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content