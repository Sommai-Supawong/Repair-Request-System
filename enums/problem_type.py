from enum import Enum


class ProblemType(str, Enum):
    ELECTRICAL = "electrical"
    FURNITURE = "furniture"
    COMPUTER = "computer"
    AIRCON = "aircon"
    OTHER = "other"

