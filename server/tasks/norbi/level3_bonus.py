from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/level3/bonus")

counter = 2024

@router.post("")
def handle_bonus():
    global counter
    response = str(counter)
    counter -= 1
    print(response)
    return Response(content="2022", media_type="text/plain")