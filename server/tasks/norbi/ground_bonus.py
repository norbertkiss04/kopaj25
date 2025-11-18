from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/ground/bonus")

counter = 5

@router.post("")
def handle_bonus():

    return Response(content=5, media_type="text/plain")