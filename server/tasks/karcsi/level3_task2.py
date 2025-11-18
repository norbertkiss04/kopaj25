from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/level3/task2")


# Egyszerűsített type chart a feladatleírás alapján
TYPE_CHART = {
    "normal": [],
    "fire": ["grass", "ice", "bug", "steel"],
    "water": ["fire", "ground", "rock"],
    "grass": ["water", "ground", "rock"],
    "electric": ["water", "flying"],
    "ice": ["grass", "ground", "flying", "dragon"],
    "fighting": ["normal", "ice", "rock", "dark", "steel"],
    "poison": ["grass", "fairy"],
    "ground": ["fire", "electric", "poison", "rock", "steel"],
    "flying": ["grass", "fighting", "bug"],
    "psychic": ["fighting", "poison"],
    "bug": ["grass", "psychic", "dark"],
    "rock": ["fire", "ice", "flying", "bug"],
    "ghost": ["psychic", "ghost"],
    "dragon": ["dragon"],
    "dark": ["psychic", "ghost"],
    "steel": ["ice", "rock", "fairy"],
    "fairy": ["fighting", "dragon", "dark"],
}
@router.post("")
async def type_advantage_finder(request: Request):
    data = await request.json()

    enemy = data.get("enemy", {})
    your_team = data.get("your_team", [])

    # Ha nincs csapat, adjunk vissza üres választ (vagy hibát, de a feladat nem kér hibakezelést)
    if not your_team:
        return JSONResponse({"best_choice": None})

    enemy_type = str(enemy.get("type", "")).strip().lower()

    best_name = your_team[0].get("name")  # alapértelmezett: első Pokémon
    strong_against_enemy = []

    # Végigmegyünk a csapaton, megnézzük, kinek van type advantage-e
    for member in your_team:
        p_name = member.get("name")
        p_type = str(member.get("type", "")).strip().lower()

        # A Pokémon erős, ha a saját típusa listájában szerepel az ellenség típusa
        strengths = TYPE_CHART.get(p_type, [])
        if enemy_type in strengths:
            strong_against_enemy.append(p_name)

    # Ha van olyan, akinek type advantage-e van, az első ilyen jó válasz
    if strong_against_enemy:
        best_name = strong_against_enemy[0]

    return JSONResponse({"best_choice": best_name})