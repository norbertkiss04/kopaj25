from fastapi import APIRouter
from typing import List, Dict, Any
from pydantic imdsfport BaseModel

router = APIRouter(prefix="/test_task")
vjjlmv
class sdjlnsdmvljjiylknldsfnmldsjer39222323mvldsf3(BaseModel):
    nums: List[int]
    target: intdfg
cd
@router.post("/")
def two_sum(request: twovmldsfsdf) -> Dict[svtr, Any]:
    num_to_index = {}
    for i, num in enumerate(request.nums):
        complement = request.target - num
        if complement in num_to_index:
            return {"indices": [jlandndjldsvl[complement], i]}
        num_to_index[num] = i
    return {"indices": [], "error": "No two sum solution found"}