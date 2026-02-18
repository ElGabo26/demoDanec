# file: rag_search.py
import json
import re
import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from openai import OpenAI


# --- cargar índice ---
INDEX_FILE = "/workspace/demoDanec/tools/kb_index.npz"
META_FILE = "/workspace/demoDanec/tools/kb_meta.json"

data = np.load(INDEX_FILE)
embeddings = data["embeddings"]  # shape: (N, dim)

with open(META_FILE, "r", encoding="utf-8") as f:
    meta = json.load(f)

# mismo modelo que en build_index.py
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_query(query: str) -> np.ndarray:
    return embed_model.encode([query])[0]  # vector (dim,)

def cosine_sim(a, b):
    return np.dot(a, b) / (norm(a) * norm(b) + 1e-10)

def retrieve_context(question: str, k: int = 5):

    q_vec = embed_query(question)
    sims = embeddings @ q_vec / (norm(embeddings, axis=1) * norm(q_vec) + 1e-10)
    # indices ordenados por similitud descendente
    top_idx = np.argsort(-sims)[:k]

    selected_chunks = [meta[i]["text"] for i in top_idx]
    return selected_chunks


def limpiar_respuesta_deepseek(texto):
    """
    Elimina los tags de pensamiento <think>...</think> y asegura
    que el texto restante esté limpio.
    """
    # 1. Eliminar todo lo que esté dentro de <think> y </think> (incluyendo los saltos de línea)
    texto_limpio = re.sub(r'<think>.*?</think>', '', texto, flags=re.DOTALL)
    
    # 2. Eliminar posibles etiquetas sueltas si quedaron
    texto_limpio = texto_limpio.replace('<think>', '').replace('</think>', '')
    
    # 3. Quitar espacios en blanco excesivos al inicio y final
    return texto_limpio.strip()



with open("./workspace/demoDanec/tools/instruccions.txt", "r", encoding="utf-8") as f:
        instruccions = f.read()
    
def build_prompt(question):
    context_chunks=retrieve_context(question)
    contexto = "\n\n---\n\n".join(context_chunks)
    prompt = (
        f"""
        Contexto relevante:\n{contexto}\n\n",
        Responde de forma clara y en español,  tomando  en cuenta las siguientes intruscciones {instruccions}
        """
    )
    return prompt
