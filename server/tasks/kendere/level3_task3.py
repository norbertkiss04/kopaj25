from fastapi import APIRouter, Request
from fastapi.responses import Response

router = APIRouter(prefix="/level3/task3")


@router.post("")
async def sudoku_check(request: Request):
    # A body egy text/plain string a Sudoku táblával (ASCII kerettel)
    body_bytes = await request.body()
    body = body_bytes.decode("utf-8")

    # 1) Sorokra bontás, csak a számjegyeket szedjük ki minden olyan sorból, ahol van 9 szám
    rows = []
    for line in body.splitlines():
        digits = [int(ch) for ch in line if ch.isdigit()]
        if len(digits) == 9:
            rows.append(digits)

    # Elvárjuk, hogy pontosan 9 sor legyen
    if len(rows) != 9:
        return Response(content="Invalid sudoku input.", media_type="text/plain")

    grid = rows  # 9x9 int mátrix

    # Segédfüggvények
    all_digits = set(range(1, 10))

    def box_index(r: int, c: int) -> int:
        """3x3-as doboz index (0-8)"""
        return (r // 3) * 3 + (c // 3)

    # 2) Először ellenőrizzük, hogy a sudoku teljesen helyes-e
    def is_valid_complete_sudoku(g):
        # Minden sor: 1..9
        for r in range(9):
            if set(g[r]) != all_digits:
                return False
        # Minden oszlop: 1..9
        for c in range(9):
            col = [g[r][c] for r in range(9)]
            if set(col) != all_digits:
                return False
        # Minden 3x3-as doboz: 1..9
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box_vals = []
                for rr in range(3):
                    for cc in range(3):
                        box_vals.append(g[br + rr][bc + cc])
                if set(box_vals) != all_digits:
                    return False
        return True

    if is_valid_complete_sudoku(grid):
        return Response(content="Sudoku is correct.", media_type="text/plain")

    # 3) Ha nem helyes, keressük meg az első hibás cellát (sor-major bejárás: 1. sor 1. oszloptól)
    for r in range(9):
        for c in range(9):
            current_val = grid[r][c]

            # A sorban a többi érték
            row_others = [grid[r][jc] for jc in range(9) if jc != c]
            # Az oszlopban a többi érték
            col_others = [grid[ir][c] for ir in range(9) if ir != r]
            # A 3x3-as doboz többi értéke
            br = (r // 3) * 3
            bc = (c // 3) * 3
            box_others = []
            for rr in range(3):
                for cc in range(3):
                    rr_abs = br + rr
                    cc_abs = bc + cc
                    if rr_abs == r and cc_abs == c:
                        continue
                    box_others.append(grid[rr_abs][cc_abs])

            row_missing = all_digits - set(row_others)
            col_missing = all_digits - set(col_others)
            box_missing = all_digits - set(box_others)

            candidate_set = row_missing & col_missing & box_missing

            # Ha pontosan egy szám illik ide, és az nem egyezik a jelenlegi értékkel,
            # akkor ez az első hibás cella.
            if len(candidate_set) == 1:
                correct_val = next(iter(candidate_set))
                if correct_val != current_val:
                    # Formátum: "X. row Y. column should have been Z."
                    result = (
                        f"{r + 1}. row {c + 1}. column should have been {correct_val}."
                    )
                    return Response(content=result, media_type="text/plain")

    # Ha idáig eljutunk, valami nem standard esettel állunk szemben
    # (pl. több hiba, vagy nem egyértelmű javítás).
    # Utolsó mentsvárként mondhatjuk, hogy helytelen, de nem tudjuk egyértelműen,
    # de a specifikáció szerint ilyen nem nagyon kellene előforduljon.
    return Response(content="Sudoku is incorrect.", media_type="text/plain")