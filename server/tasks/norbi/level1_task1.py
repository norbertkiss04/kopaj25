from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/level1/task1")

@router.post("")
async def level1_task1(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")
    lines = [line.strip() for line in body_str.split("\n") if line.strip()]
    if not lines:
        return Response(content="0 0 0 0", media_type="text/plain")
    
    elevations = []
    distances = []
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            distances.append(float(parts[0]))
            elevations.append(float(parts[1]))
            
    if not elevations:
        return Response(content="0 0 0 0", media_type="text/plain")

    total_distance = sum(distances[1:])
    max_elev = max(elevations)
    
    total_ascent = 0.0
    total_descent = 0.0
    
    for i in range(1, len(elevations)):
        diff = elevations[i] - elevations[i-1]
        if diff > 0:
            total_ascent += diff
        elif diff < 0:
            total_descent += -diff
            
    def fmt(num):
        if num == int(num):
            return str(int(num))
        return str(num)

    result = f"{fmt(total_distance)} {fmt(max_elev)} {fmt(total_ascent)} {fmt(total_descent)}"
    return Response(content=result, media_type="text/plain")