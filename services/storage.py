import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def cargar_json(nombre_archivo):
    path = DATA_DIR / nombre_archivo
    if not path.exists():
        return {} if nombre_archivo == "campos.json" else []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_json(nombre_archivo, datos):
    path = DATA_DIR / nombre_archivo
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)