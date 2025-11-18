from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from ai_example import ask_ai

router = APIRouter(prefix="/level1/task3")

@router.post("")
async def code_review(request: Request):
    body = await request.json()
    task_desc = request.headers.get('task-description', '')
    id_ = body["id"]
    code = body["code"]
    answers = body["answers"]
    
    # Construct answers string
    answers_str = "\n".join([f"{ans['letter']}: {ans['answer']}" for ans in answers])
    
    prompt = f"{task_desc}\n\nCode: {code}\n\nAnswers:\n{answers_str}\n\nExamine the provided code and the answer options, then pick the single best answer letter that correctly evaluates the snippet. Respond ONLY with the letter, nothing else."
    
    ai_response = ask_ai(prompt)
    if ai_response:
        letter = ai_response.strip().upper()
        # Assume it's one of A,B,C,D
        if letter in ['A', 'B', 'C', 'D']:
            return JSONResponse({"id": id_, "answerLetter": letter})
    
    # fallback
    return JSONResponse({"id": id_, "answerLetter": "A"})