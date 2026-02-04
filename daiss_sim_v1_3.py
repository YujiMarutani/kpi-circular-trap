import numpy as np
import matplotlib.pyplot as plt

from semantic_entropy import semantic_entropy
from daiss_robustness_check import compute_kripkean_robustness

def generate_trajectory(kind="human", steps=20, dim=16, noise=0.3):
    base = np.random.randn(dim)
    base = base / np.linalg.norm(base)

    traj = []
    current = base.copy()

    for t in range(steps):
        if kind == "human":
            jump = np.random.randn(dim) * noise
            current = current + jump
        elif kind == "ai":
            current = 0.8 * current + 0.2 * base
        elif kind == "random":
            current = np.random.randn(dim)

        current = current / (np.linalg.norm(current) + 1e-8)
        traj.append(current.copy())

    return np.array(traj)

def simulate_point(kind, steps=20, dim=16):
    traj = generate_trajectory(kind=kind, steps=steps, dim=dim)

    E = semantic_entropy(traj, window=5)
    semantic_radius = E[-1]

    idea_vector = traj[-1]
    context_vectors = traj[:-1] if len(traj) > 1 else traj
    robustness, avg_sim, var_sim = compute_kripkean_robustness(idea_vector, context_vectors)

    return semantic_radius, robustness, avg_sim, var_sim

def run_v1_3_sim():
    kinds = ["human", "ai", "random"]
    colors = {"human": "tab:blue", "ai": "tab:green", "random": "tab:red"}
    labels = {"human": "Human-like", "ai": "AI-like", "random": "Random"}

    plt.figure(figsize=(7, 6))

    for kind in kinds:
        for _ in range(20):
            x, y, _, _ = simulate_point(kind)
            plt.scatter(x, y, c=colors[kind], alpha=0.7, label=labels[kind])

    handles, labels_unique = [], []
    for h, l in zip(*plt.gca().get_legend_handles_labels()):
        if l not in labels_unique:
            handles.append(h)
            labels_unique.append(l)

    plt.legend(handles, labels_unique)
    plt.xlabel("Semantic Radius (E_t)")
    plt.ylabel("Kripkean Robustness (R_t)")
    plt.title("v1.3 — Creative Leap vs Logical Robustness")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_v1_3_sim()

