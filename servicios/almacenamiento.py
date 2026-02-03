import json
import os

from utilidades.rutas import (
    DATA_DIR,
    RUTA_CAMPOS,
    RUTA_CAMPOS_UNICOS,
    RUTA_INVENTARIO,
    RUTA_HISTORIAL,
    RUTA_PAPELERA
)



def _asegurar_archivo(ruta, valor_inicial):
    """Crea la carpeta de datos y el archivo si no existen."""

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(valor_inicial, f, indent=4, ensure_ascii=False)



# CAMPOS
def cargar_campos():
    _asegurar_archivo(RUTA_CAMPOS, {})
    with open(RUTA_CAMPOS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_campos(campos):
    with open(RUTA_CAMPOS, "w", encoding="utf-8") as f:
        json.dump(campos, f, indent=4, ensure_ascii=False)



# CAMPOS ÚNICOS
def cargar_campos_unicos():
    _asegurar_archivo(RUTA_CAMPOS_UNICOS, [])
    with open(RUTA_CAMPOS_UNICOS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_campos_unicos(campos):
    campos_limpios = sorted(set(campos))
    with open(RUTA_CAMPOS_UNICOS, "w", encoding="utf-8") as f:
        json.dump(campos_limpios, f, indent=4, ensure_ascii=False)



# INVENTARIO
def cargar_inventario():
    _asegurar_archivo(RUTA_INVENTARIO, [])
    with open(RUTA_INVENTARIO, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_inventario(inventario):
    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)



# HISTORIAL
def cargar_historial():
    _asegurar_archivo(RUTA_HISTORIAL, [])
    with open(RUTA_HISTORIAL, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_historial(historial):
    with open(RUTA_HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)



# PAPELERA
def cargar_papelera():
    _asegurar_archivo(RUTA_PAPELERA, [])
    with open(RUTA_PAPELERA, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_papelera(papelera):
    with open(RUTA_PAPELERA, "w", encoding="utf-8") as f:
        json.dump(papelera, f, indent=4, ensure_ascii=False)
