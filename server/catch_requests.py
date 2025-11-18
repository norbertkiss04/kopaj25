from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import json
import os
from datetime import datetime


class CatchRequestsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, capture_dir="captured_requests"):
        super().__init__(app)
        self.capture_dir = os.path.join(os.path.dirname(__file__), capture_dir)
        os.makedirs(self.capture_dir, exist_ok=True)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path.lstrip('/').rstrip('/')
        if not path:
            endpoint_name = 'root'
        else:
            endpoint_name = path.replace('/', '_')
        
        method = request.method.lower()
        filename = f"{endpoint_name}_{method}.json"
        filepath = os.path.join(self.capture_dir, filename)
        
        # Always read body (cached, won't re-consume)
        body_bytes = await request.body()
        body = None
        if body_bytes:
            try:
                body = json.loads(body_bytes.decode('utf-8'))
            except json.JSONDecodeError:
                # If not JSON, save as string
                body = body_bytes.decode('utf-8', errors='ignore')
        
        request_info = {
            "timestamp": datetime.now().isoformat(),
            "method": request.method,
            "path": str(request.url),
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "body": body
        }
        
        # Load existing requests
        existing = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, IOError):
                existing = []
        
        if len(existing) < 3:
            existing.append(request_info)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2, ensure_ascii=False)
            except IOError:
                pass
        
        response = await call_next(request)
        return response