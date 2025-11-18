from fastapi import APIRouter, Body

router = APIRouter(prefix="/level1/task1")

@router.post("")
def hiking_stats(body: str = Body(..., media_type="text/plain")) -> str:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    segments = []

    for line in lines:
        d, e = line.split()
        segments.append((float(d), int(e)))

    # Az első szegmens távolsága mindig 0, ezért azt kihagyjuk
    total_distance = sum(d for d, _ in segments[1:])
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
            total_descent += abs(diff)

    # Formázás: ha egész szám, akkor int-ként, különben float-ként
    def fmt(num):
        if isinstance(num, float) and num.is_integer():
            return str(int(num))
        return str(num)

    return f"{fmt(total_distance)} {max_elevation} {total_ascent} {total_descent}"