from fastapi import APIRouter, Request
from fastapi.responses import Response
import re

router = APIRouter(prefix="/level2/task2")

@router.post("")
async def translate_word(request: Request):
    body = await request.body()
    original_word = body.decode("utf-8").strip()
    task_desc = request.headers.get("task-description", "") or ""

    match = re.search(r'([^\s=]+)\s=\s([^\s=]+)', task_desc)
    if match:
        new_lang_word = match.group(2)
    else:
        new_lang_word = original_word

    return Response(content=new_lang_word, media_type="text/plain")
