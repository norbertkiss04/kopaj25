from fastapi import FastAPI
import importlib
import os

app = FastAPI()

# A folder neve, ahonnan betölti a fájlokat
MODULE_DIR = ""

# Kilistázzuk az összes .py fájlt (kivéve __init__.py)
modules = [
    f"{MODULE_DIR}.{file[:-3]}"
    for file in os.listdir(MODULE_DIR)
    if file.endswith(".py") and file != "__init__.py"
]

print("📂 Betöltendő modulok:", modules)

for mod in modules:
    try:
        m = importlib.import_module(mod)
        app.include_router(m.router)
        print(f"✅ Betöltve: {mod}")
    except Exception as e:
        print(f"⚠️ Hiba a {mod} betöltésekor: {e}")
