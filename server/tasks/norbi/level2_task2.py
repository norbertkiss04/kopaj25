from fastapi import APIRouter, Request
from fastapi.responses import Response
from ai_example import ask_ai

router = APIRouter(prefix="/level2/task2")

@router.post("")
async def translate_word(request: Request):
    body = await request.body()
    word = body.decode("utf-8").strip()
    task_desc = request.headers.get("task-description", "") or ""

    prompt = (
        f"{task_desc}\n\n"
        f"You are given a fictional constructed language.\n"
        f"There is EXACTLY ONE example mapping given above.\n"
        f"Your task is to create the translation of the following English word "
        f"in the SAME fictional language, using the example only as a style guide.\n\n"
        f"Translate: {word}\n"
        "Respond ONLY with the translated word, nothing else."
    )

    ai_response = ask_ai(prompt)
    if ai_response:
        text = ai_response.strip().split()[0]
        return Response(content=text, media_type="text/plain")

    return Response(content="", media_type="text/plain")
