from typing import Dict, Any, List

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter( prefix="")

# @router.get("/ground/task3")
# def ground3(request):
#     print(request.query_params)

@router.post("/ground/task1")
def return_status_ok(request):
    return 200