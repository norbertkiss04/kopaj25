from fastapi import APIRouter

router = APIRouter(prefix="/task1")

@router.get("/")
def task():
    return {"msg": "Hello, tjjest itt volt!"}