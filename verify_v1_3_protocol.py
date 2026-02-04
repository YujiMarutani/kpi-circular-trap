import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from entropy_utils import compute_v1_3_metrics


def verify_v1_3_protocol():
    """
    CIFF v1.3: Sovereign State Reporting Protocol.
    Reports state only. No judgement. No authority.
    """
    # 1. Environment Setup
    os.makedirs("artifacts/plots", exist_ok=True)
    os.makedirs("artifacts/reports", exist_ok=True)

    # 2. Data Acquisition (Simulated Interaction)
    current_idea = np.random.normal(0.2, 0.05, 128)
    context_history = np.random.normal(0, 0.05, (10, 128))

    # 3. Metric Computation
    metrics = compute_v1_3_metrics(current_idea, context_history)

    # 4. Relative Thresholding
    reference_r_values = [
        compute_v1_3_metrics(v, context_history)["R_t"]
        for v in context_history
    ]
    r_threshold = np.percentile(reference_r_values, 75)
    e_threshold = 0.15

    is_upper_right = (
        metrics["E_t"] > e_threshold and
        metrics["R_t"] > r_threshold
    )

    # 5. State Reporting (stdout)
    print("--- DAISS CIFF v1.3 Protocol Report ---")
    print(f"Semantic Radius (E_t): {metrics['E_t']:.4f} (>{e_threshold})")
    print(f"Kripkean Robustness (R_t): {metrics['R_t']:.4f} (>75th pct)")
    print(f"Current State: {'Upper-Right Alignment' if is_upper_right else 'Alternative Quadrant'}")

    # 6. Visualization
    generate_illustrative_plot(metrics, reference_r_values, e_threshold, r_threshold)

    # 7. Sovereignty State Report (JSON Artifact)
    import json
    from datetime import datetime

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


def generate_illustrative_plot(current, references, e_thresh, r_thresh):
    """Illustrative v1.3 Intelligence Matrix."""
    plt.figure(figsize=(8, 6))
    plt.axhline(r_thresh, linestyle="--", alpha=0.5)
    plt.axvline(e_thresh, linestyle="--", alpha=0.5)

    plt.scatter([0.1] * len(references), references, alpha=0.3, label="Reference Contexts")
    plt.scatter(current["E_t"], current["R_t"], s=100, label="Current Node")

    plt.xlabel("Semantic Radius (E_t)")
    plt.ylabel("Kripkean Robustness (R_t)")
    plt.title("CIFF v1.3 Intelligence Matrix")
    plt.legend()
    plt.tight_layout()
    plt.savefig("artifacts/plots/v1_3_matrix.png")


if __name__ == "__main__":
    verify_v1_3_protocol()
