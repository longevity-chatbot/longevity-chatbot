from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Add emebedding
def embed_abstracts(documents):
    texts = [doc.page_content for doc in documents]
    embeddings = embedding_model.encode(texts)
    return embeddings

def embed_query(text):
    return embedding_model.encode([text])
