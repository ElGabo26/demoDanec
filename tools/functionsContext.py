import os
import numpy as np
from sentence_transformers import SentenceTransformer

#importamos  el  modelo de embanding
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def split_text(text, max_chars=500, overlap=100):
    """
    Parte el texto en chunks con solapamiento.
    max_chars: tamaño aproximado de cada chunk
    overlap: solapamiento entre chunks para no cortar ideas
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks


def embed_texts(texts):
    """
    Calcula embeddings para una lista de textos.
    Retorna un np.array de shape (n_chunks, dim)
    """
    return embed_model.encode(texts, show_progress_bar=True)




