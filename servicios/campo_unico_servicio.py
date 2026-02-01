import json

from almacenamiento import (
    RUTA_CAMPOS_UNICOS,
    RUTA_CAMPOS,
    normalizar_nombre
)

from inventario_servicio import cargar_inventario
from historial_servicio import registrar_evento


def _cargar_campos_definidos():
    """Carga los campos definidos sin depender de campo_servicio."""
    try:
        with open(RUTA_CAMPOS, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _cargar_campos_unicos():
    """Carga la lista de campos marcados como únicos."""
    try:
        with open(RUTA_CAMPOS_UNICOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            return json.loads(contenido) if contenido else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _guardar_campos_unicos(campos):
    """Guarda la lista de campos únicos."""
    with open(RUTA_CAMPOS_UNICOS, "w", encoding="utf-8") as archivo:
        json.dump(sorted(set(campos)), archivo, indent=4, ensure_ascii=False)


def es_campo_unico(nombre_campo):
    """Devuelve True si el campo está marcado como único."""
    nombre = normalizar_nombre(nombre_campo)
    if not nombre:
        return False
    return nombre in _cargar_campos_unicos()


def detectar_conflictos_unicidad(nombre_campo, inventario):
    """Detecta valores duplicados para un campo en un inventario dado."""
    vistos = {}
    conflictos = []

    for idx, producto in enumerate(inventario):
        if nombre_campo not in producto:
            continue

        valor = producto[nombre_campo]
        if valor is None:
            continue

        if valor in vistos:
            conflictos.append({
                "campo": nombre_campo,
                "valor": valor,
                "productos": [vistos[valor], idx]
            })
        else:
            vistos[valor] = idx

    return conflictos


def marcar_campo_unico(nombre_campo):
    """Marca un campo como único."""
    nombre = normalizar_nombre(nombre_campo)
    if not nombre:
        return False, "Nombre de campo inválido."

    campos_definidos = _cargar_campos_definidos()
    if nombre not in campos_definidos:
        return False, f'El campo "{nombre}" no existe.'

    campos_unicos = _cargar_campos_unicos()
    if nombre in campos_unicos:
        return False, f'El campo "{nombre}" ya es único.'

    inventario = cargar_inventario()
    conflictos = detectar_conflictos_unicidad(nombre, inventario)

    if conflictos:
        return False, {
            "motivo": "conflicto_unicidad",
            "campo": nombre,
            "conflictos": conflictos
        }

    campos_unicos.append(nombre)
    _guardar_campos_unicos(campos_unicos)

    registrar_evento(
        accion="Modificación",
        entidad="campo_unico",
        antes={"campo": nombre, "unico": False},
        despues={"campo": nombre, "unico": True}
    )

    return True, None


def desmarcar_campo_unico(nombre_campo):
    """Quita la marca de campo único."""
    nombre = normalizar_nombre(nombre_campo)
    if not nombre:
        return False, "Nombre de campo inválido."

    campos_unicos = _cargar_campos_unicos()
    if nombre not in campos_unicos:
        return False, f'El campo "{nombre}" no está marcado como único.'

    campos_unicos.remove(nombre)
    _guardar_campos_unicos(campos_unicos)

    registrar_evento(
        accion="Modificación",
        entidad="campo_unico",
        antes={"campo": nombre, "unico": True},
        despues={"campo": nombre, "unico": False}
    )

    return True, None
