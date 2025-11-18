from fastapi import APIRouter, Request
from typing import Dict, Any
import sys
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from ai_example import ask_ai

router = APIRouter(prefix="/ground/task3")

@router.post("")
async def identify_language(request: Request):
    body = await request.body()
    sentence = body.decode('utf-8').strip()
    task_desc = request.headers.get('task-description', '')
    
    prompt = f"{task_desc} Respond ONLY with the first letter of the language, nothing else.\n\nSentence: {sentence}"
    
    ai_response = ask_ai(prompt)
    if ai_response:
        letter = ai_response.strip().lower()
        from fastapi.responses import Response
        return Response(content=letter, media_type="text/plain")
    else:
        from fastapi.responses import Response
        return Response(content="e", media_type="text/plain")  # fallback to English