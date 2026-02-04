import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from entropy_utils import compute_v1_3_metrics

def verify_v1_3_protocol():
    """
    CIFF v1.3: Sovereign State Reporting Protocol.
    This script reports the intelligence state without assuming judicial authority.
    """
    # 1. Environment Setup
    os.makedirs("artifacts/plots", exist_ok=True)

    # 2. Data Acquisition (Simulated Interaction)
    current_idea = np.random.normal(0.2, 0.05, 128)
    context_history = np.random.normal(0, 0.05, (10, 128)) # Increased context for statistics

    # 3. Metric Computation
    metrics = compute_v1_3_metrics(current_idea, context_history)
    
    # 4. Relative Thresholding (Non-Absolute Criteria)
    # Using 75th percentile as a benchmark for rigidity within the local context
    reference_r_values = [compute_v1_3_metrics(v, context_history)["R_t"] for v in context_history]
    r_threshold = np.percentile(reference_r_values, 75)
    e_threshold = 0.15 # Baseline for AI-gravity escape

    is_upper_right = (metrics["E_t"] > e_threshold and metrics["R_t"] > r_threshold)

    # 5. State Reporting (Not Judgment)
    print(f"--- DAISS CIFF v1.3 Protocol Report ---")
    print(f"Semantic Radius (E_t): {metrics['E_t']:.4f} (Ref: >{e_threshold})")
    print(f"Kripkean Robustness (R_t): {metrics['R_t']:.4f} (Ref: >{r_threshold:.2f} [75th percentile])")
    print(f"Current State: {'Upper-Right Alignment' if is_upper_right else 'Alternative Quadrant'}")

    # 6. Illustrative Visualization (Artifact)
    generate_illustrative_plot(metrics, reference_r_values, e_threshold, r_threshold)

    # Exit with 0 to ensure CI continuity unless a system-level failure occurs
    sys.exit(0)

def generate_illustrative_plot(current, references, e_thresh, r_thresh):
    """Generates an illustrative visualization of the intelligence matrix."""
    plt.figure(figsize=(8, 6))
    plt.axhline(r_thresh, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(e_thresh, color='gray', linestyle='--', alpha=0.5)
    
    # Plotting local reference points
    plt.scatter([0.1]*len(references), references, color='blue', alpha=0.3, label='Reference Contexts')
    # Plotting current node
    plt.scatter(current["E_t"], current["R_t"], color='red', s=100, label='Current Node')

    plt.title("Intelligence Matrix (Illustrative Visualization v1.3)")
    plt.xlabel("Semantic Radius (E_t)")
    plt.ylabel("Kripkean Robustness (R_t)")
    plt.legend()
    plt.savefig("artifacts/plots/v1_3_matrix.png")
    print(f"Visualization saved to: artifacts/plots/v1_3_matrix.png")

import numpy as np
import sys
import os
    # 7. Sovereignty State Report (JSON Artifact)
    import json
    from datetime import datetime

    os.makedirs("artifacts/reports", exist_ok=True)

    report = {
        "protocol": "CIFF v1.3",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metrics": {
            "E_t": float(metrics["E_t"]),
            "R_t": float(metrics["R_t"])
        },
        "relative_position": {
            "quadrant": "Upper-Right" if is_upper_right else "Alternative",
            "reference": "local_context_75_percentile"
        },
        "sovereignty_statement": {
            "judgement": None,
            "classification": None,
            "authority": "local_execution_only"
        },
        "note": "State report only. No normative evaluation."
    }

    with open("artifacts/reports/sovereignty_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # 8. CI Continuity
    sys.exit(0)


os.makedirs("artifacts/reports", exist_ok=True)
with open("artifacts/reports/sovereignty_report.json", "w") as f:
    json.dump(report, f, indent=2)
