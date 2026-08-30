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
    score = risk.severity * risk.probability * 10

    if risk.days_to_launch <= 30:
        score += 20
    elif risk.days_to_launch <= 60:
        score += 10

    if not risk.documentation_complete:
        score += 15

    return round(min(score, 100), 1)


def assign_status(score: float) -> str:
    if score >= 55:
        return "Critical"
    if score >= 30:
        return "Watch"
    return "On Track"


def build_report(risks: list[ProductRisk]) -> list[dict]:
    report = []

    for risk in risks:
        score = calculate_score(risk)
        item = asdict(risk)
        item["score"] = score
        item["status"] = assign_status(score)
        report.append(item)

    return sorted(report, key=lambda item: item["score"], reverse=True)

if __name__ == "__main__":
    report = build_report(RISKS)
    print(json.dumps(report, indent=2))

    # Lightweight verification
    assert report[0]["product"] == "Orion Display"
    assert report[0]["score"] == 75.0
    assert report[0]["status"] == "Critical"

    print("\nChecks passed.")
    