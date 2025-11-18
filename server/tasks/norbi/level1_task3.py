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
    task_desc = request.headers.get("task-description", "") or ""

    id_ = body["id"]
    code = body["code"]
    answers = body["answers"]

    # Gyűjtsük ki a valóban érvényes opcióbetűket (pl. ["A", "B", "C", "D"] vagy más)
    valid_letters = [str(a["letter"]).strip().upper() for a in answers if "letter" in a]
    valid_letters = [l for l in valid_letters if l]  # üresek kiszűrése
    valid_letters_set = set(valid_letters)

    # Biztonsági őr: ha valamiért üres, akkor ne omoljon össze
    if not valid_letters:
        # Fallback: legalább legyen egy default válasz
        return JSONResponse({"id": id_, "answerLetter": "A"})

    # Answers string összeépítése
    # Pl. "A: valami\nB: valami\n..."
    answers_str_lines = []
    for ans in answers:
        letter = str(ans["letter"])
        text = str(ans["answer"])
        answers_str_lines.append(f"{letter}: {text}")
    answers_str = "\n".join(answers_str_lines)

    # Prompt felépítése: explicit leírjuk, milyen betűk közül választhat
    # pl. "Choose one of: A, B, C, D."
    letters_list_str = ", ".join(valid_letters)

    prompt = (
        f"{task_desc}\n\n"
        f"Code snippet:\n{code}\n\n"
        f"Answer options:\n{answers_str}\n\n"
        f"Read the code and the answer options above carefully.\n"
        f"Choose the SINGLE best answer LETTER from the following: {letters_list_str}.\n"
        f"Respond ONLY with that single letter, nothing else."
    )

    ai_response = ask_ai(prompt)

    chosen_letter = None
    if ai_response:
        resp = ai_response.strip().upper()

        # 1) Ha egész válasz pontosan egy betű és benne van az opciókban
        if len(resp) == 1 and resp in valid_letters_set:
            chosen_letter = resp
        else:
            # 2) Próbáljuk meg az első olyan karaktert kivenni,
            # amely szerepel a valid_letters_set-ben
            for ch in resp:
                if ch in valid_letters_set:
                    chosen_letter = ch
                    break

    # Ha még mindig nincs értelmes betű, használjuk fallback-ként az első opció betűjét
    if not chosen_letter:
        chosen_letter = valid_letters[0]

    return JSONResponse({"id": id_, "answerLetter": chosen_letter})
