from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/level2/task1")


class TaskRequest(BaseModel):
    nodes: List[str]
    times: List[List[int]]
    start: str


class TaskResponse(BaseModel):
    route: List[str]
    totalTime: int


@router.post("", response_model=TaskResponse)
def solve_artifact_route(payload: TaskRequest) -> TaskResponse:
    nodes = payload.nodes
    times = payload.times
    start_name = payload.start

    n = len(nodes)
    start_idx = nodes.index(start_name)

    # Held–Karp DP for shortest Hamiltonian path starting at start_idx
    full_mask = (1 << n) - 1
    INF = float("inf")

    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    start_mask = 1 << start_idx
    dp[start_mask][start_idx] = 0

    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            if dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + times[u][v]
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    # Choose best endpoint (no need to return to start)
    best_end = -1
    best_cost = INF
    for v in range(n):
        if dp[full_mask][v] < best_cost:
            best_cost = dp[full_mask][v]
            best_end = v

    # Reconstruct route
    route_indices: List[int] = []
    mask = full_mask
    cur = best_end

    while cur != -1:
        route_indices.append(cur)
        prev = parent[mask][cur]
        mask ^= 1 << cur
        cur = prev

    route_indices.reverse()
    route = [nodes[i] for i in route_indices]

    return TaskResponse(route=route, totalTime=int(best_cost))
