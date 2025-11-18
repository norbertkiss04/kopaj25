from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter(prefix="/ground/task2")

class AlcoholRequest(BaseModel):
    beers: int
    shots: int

@router.post("")
def calculate_sobering_time(request: AlcoholRequest) -> Dict[str, float]:
    # Alkohol növekedés (‰)
    alcohol_level = request.beers * 0.15 + request.shots * 0.25

    # Lebomlási idő (óra)
    if alcohol_level <= 0:
        return {"hours": 0.0}

    hours = alcohol_level / 0.15

    return {"hours": hours}
