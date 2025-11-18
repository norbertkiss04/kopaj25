from fastapi import APIRouter

router = APIRouter(prefix="")

@router.get("/task1")
def task():
    return {"msg": "Gest request"}