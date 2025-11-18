from fastapi import APIRouter, Request
from fastapi.responses import Response
from collections import deque

router = APIRouter(prefix="/level3/task1")


@router.post("")
async def forest_fire(request: Request):
    # A body JSON: {"map": "...", "wind": "N|S|E|W"}
    data = await request.json()
    map_str = data["map"]
    wind = (data.get("wind") or "").upper()

    # Térkép sorokra bontása
    rows_list = map_str.splitlines()
    if not rows_list:
        return Response(content="0", media_type="text/plain")

    n_rows = len(rows_list)
    n_cols = len(rows_list[0])

    # Segédfüggvény határ-ellenőrzésre
    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < n_rows and 0 <= c < n_cols

    # Kiinduló tüzek (F) és ház (H) keresése
    fires = []
    house_pos = None

    for r in range(n_rows):
        row = rows_list[r]
        for c in range(n_cols):
            ch = row[c]
            if ch == "F":
                fires.append((r, c))
            elif ch == "H":
                house_pos = (r, c)

    # Ha nincs tűz vagy ház, sosem ér célba
    if not fires or house_pos is None:
        return Response(content="0", media_type="text/plain")

    # 8-irányú szomszédok
    dirs8 = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    # Kezdéskor: ha bármely F szomszédos a házzal → 1
    hr, hc = house_pos
    for fr, fc in fires:
        for dr, dc in dirs8:
            nr, nc = fr + dr, fc + dc
            if in_bounds(nr, nc) and (nr, nc) == house_pos:
                return Response(content="1", media_type="text/plain")

    # Szél iránya (N=fel, S=le, W=balra, E=jobbra)
    # Ha ismeretlen, akkor nincs extra terjedés.
    if wind == "N":
        wdr, wdc = -1, 0
    elif wind == "S":
        wdr, wdc = 1, 0
    elif wind == "W":
        wdr, wdc = 0, -1
    elif wind == "E":
        wdr, wdc = 0, 1
    else:
        wdr, wdc = 0, 0

    # Már égő cellák jelölése
    burned = [[False] * n_cols for _ in range(n_rows)]
    q = deque()
    for fr, fc in fires:
        burned[fr][fc] = True
        q.append((fr, fc))

    turns = 0

    while q:
        turns += 1
        current = list(q)
        q.clear()
        next_cells = []

        # 1) Normál terjedés 8 irányba
        for r, c in current:
            for dr, dc in dirs8:
                nr, nc = r + dr, c + dc
                if not in_bounds(nr, nc):
                    continue
                ch = rows_list[nr][nc]

                # Házat csak normál (nem szeles) lépés érhet el
                if (nr, nc) == house_pos:
                    return Response(content=str(turns), media_type="text/plain")

                # Csak fára terjedhet (^) és csak ha még nem égett
                if ch == "^" and not burned[nr][nc]:
                    burned[nr][nc] = True
                    next_cells.append((nr, nc))

        # 2) Szélhatás – extra terjedés a szél irányába
        if wdr != 0 or wdc != 0:
            for r, c in current:
                # extra egy cella a szél irányában (a normál lépésen túl)
                nr = r + 2 * wdr
                nc = c + 2 * wdc
                if not in_bounds(nr, nc):
                    continue
                ch = rows_list[nr][nc]

                # Szél nem ugorhat közvetlenül a házra
                if (nr, nc) == house_pos:
                    # kihagyjuk, házat csak normál lépés érheti el
                    continue

                if ch == "^" and not burned[nr][nc]:
                    burned[nr][nc] = True
                    next_cells.append((nr, nc))

        # Következő kör tüzei
        for cell in next_cells:
            q.append(cell)

    # Ha elfogyott a tűz és nem értük el a házat → 0
    return Response(content="0", media_type="text/plain")