from fastapi import APIRouter

router = APIRouter(prefix="/test2")

@router.get("/test2")
def hello_bence():
    return {"msg": "Hello, test itt volt!"}

