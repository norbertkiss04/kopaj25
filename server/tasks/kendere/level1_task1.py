from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/level1/task1")

# Input: raw text (each line: "distance elevation")
# Output: "total_distance max_elevation total_ascent total_descent"

@router.post("")
def hiking_stats(body: str) -> str:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    segments = []

    for line in lines:
        d, e = line.split()
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
            total_descent += -diff

    return f"{int(total_distance)} {max_elevation} {total_ascent} {total_descent}"
