from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ConversationHandler:
    def __init__(self):
        self.conversation_history = []
        self.last_context = ""
        self.last_citations = []
    
    def is_follow_up_question(self, question):
        """Use AI to determine if this is a follow-up question or needs new research"""
        if not self.conversation_history:
            return False
        
        last_qa = self.conversation_history[-1]
        
        classification_prompt = f"""Analyze this question to determine if it's a follow-up to the previous conversation or needs new research.

Previous Q&A:
Q: {last_qa['question']}
A: {last_qa['answer'][:200]}...

New question: {question}

Is this question:
A) A follow-up that can be answered using the same research context (asking for clarification, more detail, simpler explanation, different format, or building on the same topic)
B) A completely new topic that needs fresh research

Respond with only 'A' or 'B'."""
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": classification_prompt}],
                max_tokens=1,
                temperature=0
            )
            return response.choices[0].message.content.strip() == 'A'
        except:
            # Fallback to simple keyword detection
            return "can you" in question.lower() or "explain" in question.lower()
    
    def answer_follow_up(self, question):
        """Answer follow-up questions using existing context"""
        if not self.last_context:
            return None, []
        
        # Get recent conversation for context
        recent_history = self.conversation_history[-4:] if len(self.conversation_history) > 4 else self.conversation_history
        history_text = "\n".join([f"Q: {h['question']}\nA: {h['answer']}" for h in recent_history])
        
        # Detect if this is a style/format request
        style_keywords = ["simpler", "simple", "easier", "basic", "layman", "plain english", "summarize", "shorter"]
        is_style_request = any(keyword in question.lower() for keyword in style_keywords)
        
        if is_style_request and self.conversation_history:
            last_answer = self.conversation_history[-1]['answer']
            prompt = f"""Please rewrite this answer to be simpler and easier to understand:

Original answer: {last_answer}

User request: {question}

Instructions:
- Use practical and formal language
- Avoid jargon
- Keep sentences clear and concise
- Maintain the same key information
- Make it accessible to anyone"""
        else:
            prompt = f"""Based on our previous conversation and the scientific context below, please answer this follow-up question:

Previous conversation:
{history_text}

Scientific context:
{self.last_context}

Follow-up question: {question}

Instructions:
- Build upon the previous conversation
- Use the same scientific context to provide more detail
- Acknowledge this is a follow-up
- Do not greet or apologize
- Provide a concise and direct answer
- Maintain scientific accuracy"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content, self.last_citations
    
    def add_to_history(self, question, answer, citations):
        """Add Q&A to conversation history"""
        self.conversation_history.append({
            "question": question,
            "answer": answer,
            "citations": citations
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def update_context(self, context, citations):
        """Update the current research context"""
        self.last_context = context
        self.last_citations = citations