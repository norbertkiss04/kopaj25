from fastapi import APIRouter, Body, HTTPException

router = APIRouter(prefix="/level1/task1")

@router.post("")
def hiking_stats(body: str = Body(..., media_type="text/plain")) -> str:
    # Remove wrapping quotes if present (e.g. inputs like: "0 452\n5 500\n5 733")
    body = body.strip()
    if body.startswith('"') and body.endswith('"'):
        body = body[1:-1]

    # Split and clean lines
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="Empty input")

    segments = []
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail=f"Invalid line: {line}")
        try:
            d = float(parts[0])  # distance for the segment
            e = int(parts[1])    # elevation
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid numbers in line: {line}")
        segments.append((d, e))

    # --- Calculations ---

    # Total distance = ALL segment distances EXCEPT the first (which is always 0)
    total_distance = sum(d for d, _ in segments[1:])

    # Max elevation
    max_elevation = max(e for _, e in segments)

    # Ascent & descent
    total_ascent = 0
    total_descent = 0

    for i in range(1, len(segments)):
        prev_e = segments[i - 1][1]
        curr_e = segments[i][1]
        diff = curr_e - prev_e
        if diff > 0:
            total_ascent += diff
        else:
            total_descent += -diff

    # Format floats cleanly
    def fmt(num):
        if isinstance(num, float) and num.is_integer():
            return str(int(num))
        return str(num)

    return f"{fmt(total_distance)} {max_elevation} {total_ascent} {total_descent}"
