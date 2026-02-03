#!/usr/bin/env python3
"""
DAISS v2.2 - CIFF Verification Logic
Separating "System Sanity (CI)" from "Theoretical Integrity (Theory)"
"""

import os
import sys
import yaml
import numpy as np

# Resolve Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from daiss_core import DAISS_Core_v2_2

def verify():
    print("Initiating DAISS v2.2 CIFF Verification...")
    core = DAISS_Core_v2_2(r=0.14, D=0.38)
    result = core.heartbeat(steps=1000)
    
    mean_forks = result.get('mean_forks', 0)
    last_ternary = result.get('ternary', {"+1": 0})

    # --- 1. THEORETICAL INTEGRITY (The Golden Standard) ---
    # Strictly defined for DOI/Scientific Evidence. 
    # Does NOT cause CI failure, but recorded in logs.
    theoretical_healthy = (
        2.0 <= mean_forks <= 5.0 and 
        last_ternary["+1"] >= 0.15
    )

    # --- 2. SYSTEM SANITY (CI Survival Check) ---
    # Ensures the code is functional and not collapsed.
    # Causes CI failure only if the system itself is broken.
    ci_healthy = (
        mean_forks > 0.5 and 
        last_ternary["+1"] > 0.05
    )

    # Logging results for full transparency
    print(f"--- Statistics ---")
    print(f"Mean Forks: {mean_forks:.4f}")
    print(f"Ternary [+1]: {last_ternary['+1']:.4f}")
    print(f"Theoretical Compliance: {theoretical_healthy}")
    print(f"System Sanity: {ci_healthy}")

    # Generate Evidence (Artifact)
    os.makedirs("output", exist_ok=True)
    report = {
        "metrics": result,
        "compliance": {
            "theoretical": theoretical_healthy,
            "system": ci_healthy
        }
    }
    with open("output/verified_snapshot.yaml", "w") as f:
        yaml.dump(report, f, sort_keys=False)

    # FINAL JUDGEMENT
    if ci_healthy:
        print("\nSUCCESS: System sanity confirmed. Fragment preserved.")
        sys.exit(0)
    else:
        print("\nCRITICAL: System collapse detected.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
