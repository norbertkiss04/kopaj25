from fastapi import APIRouter, Request
from fastapi.responses import Response
from ai_example import ask_ai
import json

router = APIRouter(prefix="/level2/task2")

@router.post("")
async def translate_word(request: Request):
    body = await request.body()
    word = body.decode("utf-8").strip()
    task_desc = request.headers.get("task-description", "") or ""

    prompt = (
        f"{task_desc}\n\n"
        f"Translate the following English word to the new language: {word}\n"
        "Respond ONLY with the translated word, nothing else."
    )

    json_schema = {
        "name": "translation_response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "translation": {
                    "type": "string",
                    "description": "The single translated word in the target language"
                }
            },
            "required": ["translation"],
            "additionalProperties": False
        }
    }
    response_format = {
        "type": "json_schema",
        "json_schema": json_schema
    }
    ai_response = ask_ai(prompt, response_format=response_format)
    if ai_response:
        try:
            data = json.loads(ai_response.strip())
            translation = data["translation"].strip()
            return Response(content=translation, media_type="text/plain")
        except (json.JSONDecodeError, KeyError):
            text = ai_response.strip()
            first_token = text.split()[0] if text else word
            return Response(content=first_token, media_type="text/plain")
    return Response(content=word, media_type="text/plain")
