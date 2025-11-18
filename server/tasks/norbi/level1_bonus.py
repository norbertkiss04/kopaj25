from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/level1/bonus")

import os

with open(os.path.join(os.path.dirname(__file__), "popular_countries.txt"), "r") as f:
    countries = [line.strip() for line in f.readlines() if line.strip()]

index = 0

@router.post("")
def handle_bonus():

    return Response(content="Malta", media_type="text/plain")