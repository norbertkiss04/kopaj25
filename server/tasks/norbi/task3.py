from fastapi import APIRouter, Request
from pathlib import Path
import sys

# Add root directory to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from ai_example import ask_ai

router = APIRouter(prefix="/ground/task3")


@router.post("")
async def identify_language(request: Request):
    body = await request.body()
    sentence = body.decode("utf-8").strip()
    task_desc = request.headers.get("task-description", "")

    prompt = (
        f"{task_desc}\n"
        "Respond ONLY with the single first letter of the language name. "
        "No words, no punctuation, no explanation.\n\n"
        f"Sentence: {sentence}"
    )

    ai_response = ask_ai(prompt)
    from fastapi.responses import Response

    # If AI returns nothing
    if not ai_response:
        return Response(content="e", media_type="text/plain")

    # Clean up whitespace
    letter = ai_response.strip().lower()

    # Validate strict output: exactly 1 alphabetic character
    if len(letter) != 1 or not letter.isalpha():
        return Response(content="e", media_type="text/plain")

    return Response(content=letter, media_type="text/plain")
