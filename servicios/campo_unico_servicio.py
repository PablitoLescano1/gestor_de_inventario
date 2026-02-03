import json

# Rutas de almacenamiento (acceso directo para evitar imports circulares)
from almacenamiento import (
    RUTA_CAMPOS_UNICOS,
    RUTA_CAMPOS,
)

# Servicios de dominio
from inventario_servicio import cargar_inventario
from historial_servicio import registrar_evento

# Utilidades
from utilidades.texto import normalizar_nombre


# Helpers de almacenamiento (privados)
def _cargar_campos_definidos():
    """Carga los campos definidos sin depender de campo_servicio."""
    
    try:
        with open(RUTA_CAMPOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
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


# Consultas
def es_campo_unico(nombre_campo):
    """Devuelve True si el campo está marcado como único."""
    
    nombre = normalizar_nombre(nombre_campo)
    if not nombre:
        return False

    return nombre in _cargar_campos_unicos()


def detectar_conflictos_unicidad(nombre_campo, inventario):
    """Detecta valores duplicados para un campo en un inventario dado."""
    
    nombre = normalizar_nombre(nombre_campo)
    if not nombre:
        return []

    vistos = {}
    conflictos = []

    for idx, producto in enumerate(inventario):
        if nombre not in producto:
            continue

        valor = producto[nombre]
        if valor is None:
            continue

        if valor in vistos:
            conflictos.append({
                "campo": nombre,
                "valor": valor,
                "productos": [vistos[valor], idx]
            })
        else:
            vistos[valor] = idx

    return conflictos


def validar_unicidad_producto(producto, inventario):
    """
    Valida que un producto no viole restricciones de campos únicos.
    Devuelve una lista de conflictos (vacía si no hay).
    """
    
    conflictos = []

    for campo, valor in producto.items():
        if not es_campo_unico(campo):
            continue

        if valor is None:
            continue

        for idx, existente in enumerate(inventario):
            if existente.get(campo) == valor:
                conflictos.append({
                    "campo": campo,
                    "valor": valor,
                    "tipo": "unicidad",
                    "producto": idx
                })
                break

    return conflictos


# Comandos
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
