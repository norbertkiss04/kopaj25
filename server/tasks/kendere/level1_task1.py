from fastapi import APIRouter, Body

router = APIRouter(prefix="/level1/task1")

@router.post("")
def hiking_stats(body: str = Body(..., media_type="text/plain")) -> str:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    segments = []

    for line in lines:
        d, e = line.split()
        # Távolság float, magasság int (a példa alapján)
        segments.append((float(d), int(e)))

    total_distance = sum(d for d, _ in segments)
    max_elevation = max(e for _, e in segments)

    total_ascent = 0
    total_descent = 0

    for i in range(1, len(segments)):
        prev_e = segments[i - 1][1]
        curr_e = segments[i][1]

        diff = curr_e - prev_e
        if diff > 0:
            total_ascent += diff
        else:
            # abs() használata elegánsabb
            total_descent += abs(diff)

    # SEGÉDFÜGGVÉNY A FORMÁZÁSHOZ:
    # Ha a szám egész (pl. 13.0), akkor írjuk ki int-ként (13).
    # Ha tört (pl. 13.5), akkor maradjon float.
    def fmt(num):
        if isinstance(num, float) and num.is_integer():
            return str(int(num))
        return str(num)

    # Itt a javítás: nem kényszerítjük int-re a total_distance-t, hanem formázzuk
    return f"{fmt(total_distance)} {max_elevation} {total_ascent} {total_descent}"
