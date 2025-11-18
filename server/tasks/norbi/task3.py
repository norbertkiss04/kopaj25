from fastapi import APIRouter
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter( prefix="/ground/task3")

@router.post("/")
def two_sum(request: TwoSumRequest) -> Dict[str, Any]:
    return "f"