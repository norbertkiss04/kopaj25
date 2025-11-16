from fastapi import APIRouter

router = APIRouter(prefix="/test")

@router.get("/")
def hello_bence():
    return {"msg": "Hello, test itt volt!"}
