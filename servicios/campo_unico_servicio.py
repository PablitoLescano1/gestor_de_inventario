import json

from almacenamiento import RUTA_CAMPOS_UNICOS
from historial_servicio import registrar_evento


def _normalizar_nombre(nombre):
    """Normaliza nombres de campo para uso interno consistente."""
    
    if not isinstance(nombre, str):
        return None
    return " ".join(nombre.strip().split())


def _cargar_campos_unicos():
    """Carga la lista de campos marcados como únicos."""
    
    try:
        with open(RUTA_CAMPOS_UNICOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _guardar_campos_unicos(campos):
    """Guarda la lista de campos únicos."""
    
    with open(RUTA_CAMPOS_UNICOS, "w", encoding="utf-8") as archivo:
        json.dump(campos, archivo, indent=4, ensure_ascii=False)


def es_campo_unico(nombre_campo):
    """Devuelve True si el campo está marcado como único."""
    
    nombre = _normalizar_nombre(nombre_campo)
    if not nombre:
        return False

    campos_unicos = _cargar_campos_unicos()
    return nombre in campos_unicos


def marcar_campo_unico(nombre_campo):
    """Marca un campo como único."""
    
    nombre = _normalizar_nombre(nombre_campo)
    if not nombre:
        return False, "Nombre de campo inválido."

    campos_unicos = _cargar_campos_unicos()

    if nombre in campos_unicos:
        return False, f'El campo "{nombre}" ya es único.'

    estado_anterior = {
        "campo": nombre,
        "unico": False
    }

    campos_unicos.append(nombre)
    _guardar_campos_unicos(campos_unicos)

    # Historial: marcado como campo unico
    registrar_evento(
        accion="Modificación",
        entidad="campo_unico",
        antes=estado_anterior,
        despues={
            "campo": nombre,
            "unico": True
        }
    )

    return True, None


def desmarcar_campo_unico(nombre_campo):
    """Quita la marca de campo único."""
    
    nombre = _normalizar_nombre(nombre_campo)
    if not nombre:
        return False, "Nombre de campo inválido."

    campos_unicos = _cargar_campos_unicos()

    if nombre not in campos_unicos:
        return False, f'El campo "{nombre}" no está marcado como único.'

    estado_anterior = {
        "campo": nombre,
        "unico": True
    }

    campos_unicos.remove(nombre)
    _guardar_campos_unicos(campos_unicos)

    # Historial: desmarcado como campo unico
    registrar_evento(
        accion="Modificación",
        entidad="campo_unico",
        antes=estado_anterior,
        despues={
            "campo": nombre,
            "unico": False
        }
    )

    return True, None
