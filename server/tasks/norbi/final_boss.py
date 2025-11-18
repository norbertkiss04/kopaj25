from fastapi import APIRouter, Response

router = APIRouter(prefix="/final-boss")

@router.post("")
def final_boss():
    return Response(content="I accept the terms and conditions", media_type="text/plain")