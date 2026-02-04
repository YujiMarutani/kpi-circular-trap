import numpy as np

def compute_kripkean_robustness(idea_vector, context_vectors):
    """
    Computes Kripkean Robustness (R_t):
    fixed-designator stability across perturbed contexts.
    """
    similarities = []
    v = idea_vector / (np.linalg.norm(idea_vector) + 1e-8)

    for ctx in context_vectors:
        c = ctx / (np.linalg.norm(ctx) + 1e-8)
        sim = np.dot(v, c)
        similarities.append(sim)

    similarities = np.array(similarities)
    avg_sim = similarities.mean()
    var_sim = similarities.var()

    robustness = avg_sim / (var_sim + 1e-6)
    return robustness, avg_sim, var_sim

