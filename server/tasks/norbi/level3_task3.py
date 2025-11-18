from fastapi import APIRouter, Request
from fastapi.responses import Response
from pathlib import Path
import sys
import re

# --- AI modul importálása (ahogy a példádban volt) ---
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from ai_example import ask_ai

router = APIRouter(prefix="/level3/task3")

@router.post("")
async def find_picture_id_with_ai(request: Request):
    # 1. Kérés törzsének beolvasása (a tárgy neve)
    body = await request.body()
    object_name = body.decode("utf-8").strip()
    
    # Ha van task description header, azt is felhasználhatjuk, de itt a képek tartalma a lényeg.
    
    # 2. A Prompt összeállítása
    # Leírjuk az AI-nak, mi van az 5 képen (a PDF alapján).
    prompt = (
        "I have 5 pictures containing specific objects. Your task is to identify which picture contains the user's object.\n\n"
        "Picture 1: Apple, blue sneakers (shoes), camera, binoculars, glasses, watch, coffee mug, pencil.\n"
        "Picture 2: Autumn leaf, globe, headphones, lantern, ruler, party hat, pinecone, scissors, gift box, flashlight, lego block.\n"
        "Picture 3: Game controller, medicine bottle (pills), chess pawn, travel mug (thermos), calculator, alarm clock, lightbulb, green notebook, band-aid.\n"
        "Picture 4: Toothbrush, spoon, hammer, banana, candles, seashell, paperclip, paintbrush, magnet, dice.\n"
        "Picture 5: Eraser, chess clock, feather, compass (drawing tool), tea bag, soap bar, tennis ball, origami crane.\n\n"
        f"User's object: \"{object_name}\"\n\n"
        "Question: Which Picture number (1-5) contains this object?\n"
        "Respond ONLY with the single number (e.g., 1). No text, no explanation."
    )

    # 3. AI megkérdezése
    ai_response = ask_ai(prompt)

    # 4. Válasz feldolgozása
    if not ai_response:
        # Ha nincs válasz, tippelünk vagy 0-t adunk vissza (hiba)
        return Response(content="0", media_type="text/plain")

    # Megpróbáljuk kinyerni a számot a válaszból (biztonsági okból, ha az AI szöveget is írna)
    match = re.search(r'[1-5]', ai_response)
    if match:
        result = match.group(0)
    else:
        result = "1" # Ha nem talált 1-5 közötti számot

    return Response(content=result, media_type="text/plain")