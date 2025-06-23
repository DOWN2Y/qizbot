# src/vector_store.py

import faiss
import numpy as np
from typing import List

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add(self, vectors: List[List[float]], docs: List[str]):
        self.index.add(np.array(vectors).astype('float32'))
        self.documents.extend(docs)

    def search(self, query_vector: List[float], top_k=3):
        D, I = self.index.search(np.array([query_vector]).astype('float32'), top_k)
        return [self.documents[i] for i in I[0]]