from fastapi import FastAPI
import importlib
import pkgutil
import logging
import sys
import os

# Add the server directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tasks

# Get the uvicorn logger which is already configured
logger = logging.getLogger("uvicorn")

app = FastAPI()

# Log successful endpoint loading
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