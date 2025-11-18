from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/level2/bonus")

@router.post("")
def handle_bonus():
    return Response(content="2025-11-27", media_type="text/plain")