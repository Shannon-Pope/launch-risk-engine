from dataclasses import dataclass

@dataclass
class ProductRisk:
    product: str
    severity: int
    probability: float

def calculate_score(risk: ProductRisk) -> float:
    ...
    