import os
from openai import OpenAI
from rag.qa_pipeline import generate_context

client = OpenAI(api_key="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")

# Prompt LLM 
def ask_with_relevant_context(question, vectorstore):
    context = generate_context(vectorstore, question)

    prompt = f"""Use the following scientific context to answer the question:

{context}

Q: {question}
A:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
