from http import HTTPStatus
from typing import Dict, Any, List

from fastapi import APIRouter, Request
from pydantic import BaseModel


router = APIRouter( prefix="/ground/task1")

# @router.get("/ground/task3")
# def ground3(request):
#     print(request.query_params)

@router.post("")
def return_status_ok(request: Request):
    return HTTPStatus.OK