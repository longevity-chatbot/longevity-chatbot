import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedder import embed_query

# find most relevant papers based on cosine similarity
def retrieve_top_k(user_question, papers, embeddings, k=3):
    query_embedding = embed_query(user_question)
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:k]
    return [papers[i] for i in top_indices]
