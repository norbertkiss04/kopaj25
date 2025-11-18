from fastapi import APIRouter, Body

router = APIRouter(prefix="/level1/task1")


@router.post("")
async def hiking_stats(body: str = Body(..., media_type="text/plain")):
    lines = body.strip().splitlines()

    distances = []
    elevations = []

    for line in lines:
        d_str, h_str = line.split()
        distances.append(int(d_str))
        elevations.append(int(h_str))

    total_distance = sum(distances)
    max_elevation = max(elevations)

    total_ascent = 0
    total_descent = 0

    for i in range(1, len(elevations)):
        diff = elevations[i] - elevations[i - 1]
        if diff > 0:
            total_ascent += diff
        elif diff < 0:
            total_descent -= diff  # vagy: total_descent += -diff

    # a feladat szerint egyetlen stringet kell visszaadni
    return f"{total_distance} {max_elevation} {total_ascent} {total_descent}"
