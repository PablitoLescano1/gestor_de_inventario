import json
from datetime import datetime

from almacenamiento import RUTA_HISTORIAL


def cargar_historial():
    """Carga el historial completo de eventos."""
    
    try:
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_historial(historial):
    """Guarda la lista de eventos del historial."""
    
    with open(RUTA_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)


def _generar_id_evento(historial):
    """Genera un ID incremental para el evento."""
    
    return f"evt_{len(historial) + 1:06d}"


def registrar_evento(accion, entidad, antes=None, despues=None, meta=None):
    """Registra un evento en el historial."""

    historial = cargar_historial()

    ahora = datetime.now()

    evento = {
        "id": _generar_id_evento(historial),
        "timestamp": {
            "humano": ahora.strftime("%d/%m/%Y %H:%M"),
            "iso": ahora.isoformat(timespec="seconds")
        },
        "accion": accion,
        "entidad": entidad,
        "antes": antes,
        "despues": despues,
        "meta": meta or {}
    }

    historial.append(evento)
    guardar_historial(historial)

    return True
