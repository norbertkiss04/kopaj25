from fastapi import APIRouter
from fastapi.responses import Response


router = APIRouter(prefix="/level1/task2")

def zigzag_tree_solve(arr):
    """
    arr: list[int] – a bináris fa level-order reprezentációja, -1 üres csomópont.
    Visszatérés: a csomópontok zigzag sorrendben.
    """
    if not arr:
        return []

    # A gyökér üres -> üres kimenet
    if arr[0] == -1:
        return []

    result = []
    current_level = [0]  # indexek
    left_to_right = True

    while current_level:
        next_level = []
        level_values = []

        for idx in current_level:
            if idx >= len(arr):
                continue
            value = arr[idx]
            if value == -1:
                continue
            level_values.append(value)

            # gyermekek indexei
            left = 2 * idx + 1
            right = 2 * idx + 2

            # -1 esetén a csomópontnak nincsenek gyermekei → csak akkor adjuk hozzá,
            # ha a gyermekindex létezik ÉS nem -1.
            if left < len(arr) and arr[left] != -1:
                next_level.append(left)
            if right < len(arr) and arr[right] != -1:
                next_level.append(right)

        if not level_values:
            break

        if not left_to_right:
            level_values.reverse()

        result.extend(level_values)
        left_to_right = not left_to_right
        current_level = next_level

    return result


@router.post("")
def zigzag_tree(request):
    return zigzag_tree_solve(request)