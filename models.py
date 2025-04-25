from pydantic import BaseModel
from typing import List

class ParlayLeg(BaseModel):
    match: str
    bet: str
    result: str

class Parlay(BaseModel):
    wager: float
    odds: float
    legs: List[ParlayLeg]
    status: str = "pending"
