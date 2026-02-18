# file: build_index.py
import os
import json
import numpy as np
from functionsContext import split_text, embed_texts
from readDocumentsPath  import get_file_content_from_path

DOCS_FOLDER = "./ModeloGabriel/tools/context"
INDEX_FILE = "kb_index.npz"   # archivo donde se guarda el índice
META_FILE = "kb_meta.json"    # metadatos con textos y origen

all_chunks = []
meta = []   # lista de diccionarios: {"doc": ..., "chunk": ..., "text": ...}

for filename in os.listdir(DOCS_FOLDER):
    print(filename)
    try:
        path=DOCS_FOLDER+'/'+filename
        text=get_file_content_from_path(path)
        print(len(text))
    except:
        continue

    chunks = split_text(text, max_chars=700, overlap=100)
    for i, ch in enumerate(chunks):
        all_chunks.append(ch)
        meta.append({
            "doc": filename,
            "chunk": i,
            "text": ch
        })

print(f"Total de chunks: {len(all_chunks)}")

# 1. Embeddings de todos los chunks
embeddings = embed_texts(all_chunks)  # shape: (N, dim)

# 2. Guardar embeddings + metadata
np.savez(INDEX_FILE, embeddings=embeddings)
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("Índice guardado en:", INDEX_FILE, "y metadata en:", META_FILE)
