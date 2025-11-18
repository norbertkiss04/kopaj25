from fastapi import APIRouter, Body

router = APIRouter(prefix="/level1/task1")


@router.post("")
def hiking_stats(body: str = Body(..., media_type="text/plain")) -> str:
    # Sorok szétbontása és tisztítása
    lines = [line.strip() for line in body.splitlines() if line.strip()]

    # Minden sor: "distance elevation"
    # distance = a MEGELŐZŐ ponttól mért szakasz hossza (km)
    # az első sorban a distance mindig 0
    segments: list[tuple[int, int]] = []
    for line in lines:
        d_str, e_str = line.split()
        distance = int(d_str)
        elevation = int(e_str)
        segments.append((distance, elevation))

    # Ha valamiért nincs adat, adjunk 0-ás statisztikát
    if not segments:
        return "0 0 0 0"

    # Össztáv: az első sor (0 km) után következő szakaszok távjainak összege
    total_distance = sum(d for d, _ in segments[1:])

    # Maximális tengerszint feletti magasság
    max_elevation = max(e for _, e in segments)

    # Szintkülönbségek
    total_ascent = 0
    total_descent = 0

    for i in range(1, len(segments)):
        prev_e = segments[i - 1][1]
        curr_e = segments[i][1]
        diff = curr_e - prev_e
        if diff > 0:
            total_ascent += diff
        else:
            total_descent += -diff  # diff negatív

    # Kimeneti formátum: "total_distance max_elevation total_ascent total_descent"
    return f"{total_distance} {max_elevation} {total_ascent} {total_descent}"
