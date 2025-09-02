from dataclasses import dataclass

RULESET_VERSION = "v1"
QUOTE_TTL_DAYS = 7

BASE_PRICES = {"OSAGO": 1000, "KASKO": 5000}  # валюта — TJS

AGE_RANGES = [
    (18, 21, 1.6),
    (22, 25, 1.3),
    (26, 60, 1.0),
    (61, 120, 1.2),
]

EXP_RANGES = [
    (0, 0, 1.5),   # без стажа
    (1, 3, 1.2),
    (4, 100, 1.0),
]

CAR_COEF = {"sedan": 1.00, "suv": 1.15, "truck": 1.25, "sport": 1.40}


def pick_from_ranges(value: int, ranges: list[tuple[int, int, float]]) -> float:
    for lo, hi, coef in ranges:
        if lo <= value <= hi:
            return coef
    return 1.0


@dataclass
class Calculated:
    base: float
    c_age: float
    c_exp: float
    c_car: float
    total: float
