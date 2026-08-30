from dataclasses import dataclass, asdict
from typing import Any
import json


@dataclass
class ProductRisk:
    product: str
    severity: int              # 1–5
    probability: float         # 0.0–1.0
    days_to_launch: int
    documentation_complete: bool


RISKS = [
    ProductRisk("Orion Display", 5, 0.80, 21, False),
    ProductRisk("Nova Audio", 3, 0.45, 55, True),
    ProductRisk("Atlas Mobility", 4, 0.60, 80, False),
]

def calculate_score(risk: ProductRisk) -> float:
    """Return a risk score from 0 to 100."""
    # Base score: severity (1-5) weighted by probability (0.0-1.0), scaled to 0-50.
    score = risk.severity * risk.probability * 10

    # Urgency points: the sooner the launch, the more pressure.
    if risk.days_to_launch < 30:
        score += 20
    elif risk.days_to_launch < 60:
        score += 10

    # Incomplete documentation adds fixed risk.
    if not risk.documentation_complete:
        score += 15

    return round(score, 1)

def assign_status(score: float) -> str:
    """Translate a numeric score into a readiness status."""
    if score >= 55:
        return "Critical"
    if score >= 30:
        return "Watch"
    return "On Track"

def build_report(risks: list[ProductRisk]) -> list[dict[str, Any]]:
    report: list[dict[str, Any]] = []

    for risk in risks:
        score = calculate_score(risk)
        status = assign_status(score)

        entry = asdict(risk)
        entry["score"] = score
        entry["status"] = status
        report.append(entry)

    report.sort(key=lambda entry: entry["score"], reverse=True)
    return report

if __name__ == "__main__":
    report = build_report(RISKS)
    print(json.dumps(report, indent=2))

    # Lightweight verification
    assert report[0]["product"] == "Orion Display"
    assert report[0]["score"] == 75.0
    assert report[0]["status"] == "Critical"

    print("\nChecks passed.")