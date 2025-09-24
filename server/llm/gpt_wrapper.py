import os
from openai import OpenAI
from .qa_pipeline import generate_context
from .conversation_handler import ConversationHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variable for API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=api_key)

# Global conversation handler
conversation = ConversationHandler()

def ask_with_relevant_context(question, vectorstore):
    # Check if this is a follow-up question
    if conversation.is_follow_up_question(question):
        answer, citations = conversation.answer_follow_up(question)
        if answer:  # Successfully answered as follow-up
            conversation.add_to_history(question, answer, citations)
            return answer, citations
    
    # New research question - fetch fresh context
    context, citations = generate_context(vectorstore, question)
    conversation.update_context(context, citations)

    # Create citation reference list for the AI (internal use only)
    citation_refs = "\n".join([f"[{c['id']}] {c['apa_format']}" for c in citations])
    
    prompt = f"""Use the following scientific context to answer the question:

{context}

Reference Citations (for internal use):
{citation_refs}

Instructions:
- Answer the user's question directly using only the context provided above.
- Focus specifically on what the user asked - don't drift into unrelated topics.
- If the context doesn't directly address the question, say so clearly.
- When referencing studies, use citation numbers [1], [2], etc. that match the reference list.
- Only reference citations that exist in the reference list above.
- Write in clear, layman-friendly language suitable for educated non-experts.

Q: {question}
A:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    conversation.add_to_history(question, answer, citations)
    return answer, citations
