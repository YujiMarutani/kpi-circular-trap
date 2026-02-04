import numpy as np

def semantic_entropy(embeddings, window=5):
    """
    Computes Semantic Radius (E_t):
    the average distance from the centroid of the recent embedding window.
    """
    entropies = []
    embeddings = np.array(embeddings)

    for t in range(len(embeddings)):
        start = max(0, t - window + 1)
        window_vecs = embeddings[start:t+1]

        centroid = window_vecs.mean(axis=0)
        distances = np.linalg.norm(window_vecs - centroid, axis=1)
        E_t = distances.mean()
        entropies.append(E_t)

    return np.array(entropies)

