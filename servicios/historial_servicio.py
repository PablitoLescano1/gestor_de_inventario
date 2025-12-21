from datetime import datetime

from servicios.almacenamiento import (
    cargar_historial,
    guardar_historial
)


def _generar_id_evento(historial):
    """Genera un ID incremental y estable para el evento."""

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

    return evento
