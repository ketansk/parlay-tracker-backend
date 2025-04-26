from pydantic import BaseModel, ConfigDict
from typing import Any, Dict, List, Optional
from enum import Enum
from uuid import UUID


class ParlayStatus(Enum):
    PENDING = "pending"
    WIN = "win"
    LOSS = "loss"


class ParlayLeg(BaseModel):
    game_id: str
    bet: str
    result: str = ""


class Parlay(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    user_id: str
    wager: float
    odds: float
    legs: List[ParlayLeg]
    status: ParlayStatus = "pending"
    parlay_id: Optional[UUID] = None
    metadata: Optional[Dict[str, str]] = {}
