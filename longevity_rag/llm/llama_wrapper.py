from llama_cpp import Llama

def load_llama_model():
    path = r"C:\Users\User\Desktop\longevity_rag_project\longevity_rag\llm\llama-2-7b-chat.Q4_K_M.gguf"
    print("Loading model from:", path)
    return Llama(
        model_path=path,
        n_ctx=2048,
        n_threads=8,
        verbose=True
    )

