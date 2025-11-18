from fastapi import APIRouter, Body, HTTPException

router = APIRouter(prefix="/level1/task1")

@router.post("")
def hiking_stats(body: str = Body(..., media_type="text/plain")) -> str:
    # Sorok tisztítása
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="Empty input")

    segments = []
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail=f"Invalid line: {line}")
        try:
            d = float(parts[0])
            e = int(parts[1])
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid numbers in line: {line}")
        segments.append((d, e))

    # Az első sor d = 0 -> csak a többi távolság számít
    total_distance = sum(d for d, _ in segments[1:])

    max_elevation = max(e for _, e in segments)

    total_ascent = 0
    total_descent = 0

    # Emelkedés és ereszkedés számítása
    for i in range(1, len(segments)):
        prev_e = segments[i - 1][1]
        curr_e = segments[i][1]
        diff = curr_e - prev_e
        if diff > 0:
            total_ascent += diff
        else:
            total_descent += -diff

    # Formázás: ha float egész, int-ként ad vissza
    def fmt(num):
        if isinstance(num, float) and num.is_integer():
            return str(int(num))
        return str(num)

    return f"{fmt(total_distance)} {max_elevation} {total_ascent} {total_descent}"
