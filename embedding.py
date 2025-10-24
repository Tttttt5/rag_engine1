# embedding.py
from collections import Counter
import math

_corpus = []

def add_to_corpus(texts):
    global _corpus
    _corpus.extend(texts)

def _tfidf_vector(text):
    """Tiny custom embedding vector using TF-IDF-like weights."""
    words = text.lower().split()
    tf = Counter(words)
    total_docs = len(_corpus)
    vec = {}
    for w in tf:
        df = sum(1 for doc in _corpus if w in doc)
        idf = math.log((1 + total_docs) / (1 + df)) + 1
        vec[w] = tf[w] * idf
    return vec

def get_corpus_embeddings():
    """Return one embedding vector (dict) per document."""
    return [_tfidf_vector(doc) for doc in _corpus]