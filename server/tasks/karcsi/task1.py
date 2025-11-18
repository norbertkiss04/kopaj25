from fastapi import APIRouter
from fastapi.responses import Response


router = APIRouter(prefix="/ground/task1")


@router.post("")
def return_status_ok():
    return Response(status_code=200)