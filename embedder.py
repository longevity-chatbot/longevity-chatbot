from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Add emebedding
def embed_abstracts(papers):
    abstracts = [p['summary'] for p in papers]
    embeddings = model.encode(abstracts)
    return embeddings

def embed_query(text):
    return model.encode([text])