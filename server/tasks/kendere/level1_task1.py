from fastapi import APIRouter, Body, HTTPException

router = APIRouter(prefix="/level1/task1")

@router.post("")
def hiking_stats(body: str = Body(..., media_type="text/plain")):
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="Empty body")

    total_distance = 0
    max_elevation = None
    total_ascent = 0
    total_descent = 0

    prev_elev = None

    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail=f"Invalid line: '{line}'")
        try:
            dist = int(parts[0])
            elev = int(parts[1])
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid numbers in line: '{line}'")

        total_distance += dist

        if max_elevation is None or elev > max_elevation:
            max_elevation = elev

        if prev_elev is not None:
            diff = elev - prev_elev
            if diff > 0:
                total_ascent += diff
            elif diff < 0:
                total_descent += -diff

        prev_elev = elev

    result = f"{total_distance} {max_elevation} {total_ascent} {total_descent}"
    return result
