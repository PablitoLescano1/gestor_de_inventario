import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "datos"))

# archivos 
RUTA_CAMPOS = os.path.join(DATA_DIR, "campos.json")
RUTA_CAMPOS_UNICOS = os.path.join(DATA_DIR, "campos_unicos.json")

RUTA_INVENTARIO = os.path.join(DATA_DIR, "inventario.json")

RUTA_HISTORIAL = os.path.join(DATA_DIR, "historial.json")
