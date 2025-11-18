from fastapi import APIRouter
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/task2")

class TwoSumRequest(BaseModel):
    nums: List[int]
    target: int

@router.post("/")
def two_sum(request: TwoSumRequest) -> Dict[str, Any]:
    num_to_index = {}
    for i, num in enumerate(request.nums):
        complement = request.target - num
        if complement in num_to_index:
            return {"indices": [num_to_index[complement], i]}
        num_to_index[num] = i
    return {"indices": [], "error": "No two sum solution asd."}