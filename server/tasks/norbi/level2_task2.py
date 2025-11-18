from fastapi import APIRouter, Request
from fastapi.responses import Response
from pathlib import Path
import sys

# Add root directory to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from ai_example import ask_ai

router = APIRouter(prefix="/level2/task2")

@router.post("")
async def translate_word(request: Request):
    body = await request.body()
    word = body.decode("utf-8").strip()
    task_desc = request.headers.get("task-description", "")

    prompt = f"{task_desc}\n\nTranslate the following English word to the new language: {word}\nRespond ONLY with the translated word in the new language, nothing else."

    ai_response = ask_ai(prompt)
    translation = ai_response.strip() if ai_response else word
    return Response(content=translation, media_type="text/plain")