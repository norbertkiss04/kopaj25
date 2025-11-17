from fastapi import APIRouter

router = APIRouter(prefix="/task2")

@router.get("/")
def task():
    return {"msg": "Hello,  itt volt!"}