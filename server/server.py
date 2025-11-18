from fastapi import FastAPI
import importlib
import pkgutil
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tasks

logger = logging.getLogger("uvicorn")

app = FastAPI()
ENABLE_CATCH_REQUESTS = True

if ENABLE_CATCH_REQUESTS:
    from .catch_requests import CatchRequestsMiddleware
    app.add_middleware(CatchRequestsMiddleware, capture_dir="captured_requests")

for _, name, _ in pkgutil.walk_packages(tasks.__path__, prefix="tasks."):
    try:
        mod = importlib.import_module(name)
        router = getattr(mod, "router", None)
        if router:
            app.include_router(router)
            logger.info(f"Successfully loaded endpoint: {router.prefix}")
        else:
            logger.warning(f"Module {name} loaded but no router found")
    except Exception as e:
        logger.error(f"Unexpected error loading module {name}: {e}")