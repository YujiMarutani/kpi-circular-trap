import numpy as np
import networkx as nx

class DAISSCore:
    def __init__(self, N=100, r=0.14, D=0.38, seed=42):
        self.N = N
        self.r = r
        self.D = D
        np.random.seed(seed)
        # Initialize Topology
        self.G = nx.barabasi_albert_graph(N, 3, seed=seed)
        # Sovereignty states
        self.s = np.random.normal(1.0, 0.2, N)

    def step(self):
        new_s = self.s.copy()
        for i in range(self.N):
            neighbors = list(self.G.neighbors(i))
            if not neighbors: continue
            # Reaction-Diffusion Dynamics
            diffusion = self.D * np.mean([self.s[j] - self.s[i] for j in neighbors])
            reaction = self.r * self.s[i] * (1 - self.s[i] / 5.0)
            new_s[i] += reaction + diffusion
        self.s = np.clip(new_s, 0.1, 5.0)

    def run(self, steps=1000):
        """Simulation Engine for History Collection"""
        history = {"forks": [], "ternary": []}
        for _ in range(steps):
            self.step()
            counts = {
                "+1": np.sum(self.s > 1.5), 
                "0": np.sum((self.s >= 0.8) & (self.s <= 1.5)), 
                "-1": np.sum(self.s < 0.8)
            }
            # Calculate metrics
            history["forks"].append(np.sum(self.s > 3.0) / 10.0)
            history["ternary"].append({k: v/self.N for k, v in counts.items()})
        return history

class DAISS_Core_v2_2(DAISSCore):
    """
    Official CIFF / DOI Interface
    DAISS v2.2 Canonical Contract
    """
    def heartbeat(self, steps=1000):
        history = self.run(steps)
        # Evaluate last 200 steps
        forks = np.array(history["forks"][-200:])
        mean_forks = float(np.mean(forks))
        last_ternary = history["ternary"][-1]
        
        # Stability Criteria
        healthy = (2.0 <= mean_forks <= 5.0 and last_ternary["+1"] >= 0.15)
        
        return {
            "status": "Healthy" if healthy else "Unhealthy",
            "mean_forks": mean_forks,
            "ternary": last_ternary
        }
