import os

# Directorio base del proyecto (raíz)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpeta de datos
DATA_DIR = os.path.join(BASE_DIR, "datos")

# Archivos principales
RUTA_CAMPOS = os.path.join(DATA_DIR, "campos.json")
RUTA_CAMPOS_UNICOS = os.path.join(DATA_DIR, "campos_unicos.json")
RUTA_INVENTARIO = os.path.join(DATA_DIR, "inventario.json")
RUTA_HISTORIAL = os.path.join(DATA_DIR, "historial.json")


def asegurar_estructura():
    """Crea carpetas y archivos base si no existen."""

    os.makedirs(DATA_DIR, exist_ok=True)

    archivos_base = {
        RUTA_CAMPOS: {},
        RUTA_CAMPOS_UNICOS: [],
        RUTA_INVENTARIO: [],
        RUTA_HISTORIAL: []
    }

    for ruta, contenido_inicial in archivos_base.items():
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as f:
                import json
                json.dump(contenido_inicial, f, indent=4, ensure_ascii=False)
                