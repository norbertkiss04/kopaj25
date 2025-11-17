from fastapi import APIRouter

router = APIRouter(prefix="/task3")

@router.get("/")
def task():
    return {"msg": "Hello, tjjest itt volt!"}