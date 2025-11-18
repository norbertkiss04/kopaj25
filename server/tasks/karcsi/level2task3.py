from fastapi import APIRouter, Request
from fastapi.responses import Response
import sys
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from ai_example import ask_ai

router = APIRouter(prefix="/level2/task3")


@router.post("")
async def find_object_image(request: Request):
    raw_body = await request.body()
    object_desc = raw_body.decode("utf-8").strip()

    # Task description header – ebben van a link is
    task_desc = request.headers.get("task-description", "") or ""

    # Prompt felépítése
    # task_desc már tartalmazza: "Return ONLY the ID (number)... <link>"
    # Ráerősítünk, hogy csak 1–5 közötti számjegy legyen a válasz.
    prompt = (
        f"{task_desc}\n\n"
        f"Object to look for: {object_desc}\n\n"
        "There are exactly 5 images, numbered 1 to 5.\n"
        "Identify on which single image (1–5) the given object appears.\n"
        "Respond ONLY with a single digit from 1 to 5, nothing else."
    )

    ai_response = ask_ai(prompt)

    chosen_digit = None
    if ai_response:
        resp = ai_response.strip()

        # 1) Ha a teljes válasz pontosan egy karakter és 1–5 közötti számjegy
        if len(resp) == 1 and resp in "12345":
            chosen_digit = resp
        else:
            # 2) Keresd meg az első 1–5 közötti számjegyet a válaszban
            for ch in resp:
                if ch in "12345":
                    chosen_digit = ch
                    break

    # Ha az AI nem adott érvényes számot, fallback: 1
    if chosen_digit is None:
        chosen_digit = "1"

    # Válasz: csak a szám, text/plain
    return Response(content=chosen_digit, media_type="text/plain")
