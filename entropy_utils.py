import numpy as np
from scipy.stats import entropy

def normalized_entropy_diff(human_dist, ai_dist):
    """
    Compute normalized entropy difference:
        diff = H(human) - H(ai)
        normalized = diff / max(H(human), H(ai))
    Only positive differences contribute to sovereignty (χ boost).
    """

    h = np.array(human_dist, dtype=float)
    a = np.array(ai_dist, dtype=float)

    h = h / h.sum()
    a = a / a.sum()

    H_h = entropy(h)
    H_a = entropy(a)

    diff = H_h - H_a
    norm = diff / max(H_h, H_a)

    # Sovereignty trace: only positive deviation
    return max(norm, 0.0)
