import json

from almacenamiento import RUTA_CAMPOS_UNICOS
from inventario_servicio import cargar_inventario
from campo_servicio import cargar_campos
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
    
    campos_ordenados = sorted(set(campos))
    with open(RUTA_CAMPOS_UNICOS, "w", encoding="utf-8") as archivo:
        json.dump(campos_ordenados, archivo, indent=4, ensure_ascii=False)


def es_campo_unico(nombre_campo):
    """Devuelve True si el campo está marcado como único."""
    
    nombre = _normalizar_nombre(nombre_campo)
    if not nombre:
        return False

    campos_unicos = _cargar_campos_unicos()
    return nombre in campos_unicos


def _detectar_conflictos_unicidad(nombre_campo):
    """Detecta valores duplicados en inventario para un campo dado."""
    
    inventario = cargar_inventario()
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
    
    nombre = _normalizar_nombre(nombre_campo)
    if not nombre:
        return False, "Nombre de campo inválido."

    campos_definidos = cargar_campos()
    if nombre not in campos_definidos:
        return False, f'El campo "{nombre}" no existe.'

    campos_unicos = _cargar_campos_unicos()
    if nombre in campos_unicos:
        return False, f'El campo "{nombre}" ya es único.'

    conflictos = _detectar_conflictos_unicidad(nombre)
    if conflictos:
        return False, {
            "motivo": "conflicto_unicidad",
            "campo": nombre,
            "conflictos": conflictos,
            "accion_sugerida": "resolver_valores_duplicados"
        }

    campos_unicos.append(nombre)
    _guardar_campos_unicos(campos_unicos)

    registrar_evento(
        accion="Modificación",
        entidad="campo_unico",
        antes={
            "campo": nombre,
            "unico": False
        },
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

    campos_unicos.remove(nombre)
    _guardar_campos_unicos(campos_unicos)

    registrar_evento(
        accion="Modificación",
        entidad="campo_unico",
        antes={
            "campo": nombre,
            "unico": True
        },
        despues={
            "campo": nombre,
            "unico": False
        }
    )

    return True, None


def restaurar_campo_unico(nombre_campo, permitir_conflictos=False):
    """Restaura la unicidad de un campo eliminado.
    Si hay conflictos y permitir_conflictos=False: no restaura.
    Si permitir_conflictos=True: restaura y marca como conflictivo."""
        
    nombre = _normalizar_nombre(nombre_campo)
    if not nombre:
        return False, "Nombre de campo inválido."

    campos_definidos = cargar_campos()
    if nombre not in campos_definidos:
        return False, f'El campo "{nombre}" no existe.'

    campos_unicos = _cargar_campos_unicos()
    if nombre in campos_unicos:
        return False, "El campo ya es único."

    conflictos = _detectar_conflictos_unicidad(nombre)
    if conflictos and not permitir_conflictos:
        return False, {
            "motivo": "conflicto_restauracion_unicidad",
            "campo": nombre,
            "conflictos": conflictos,
            "restaurado": False
        }

    campos_unicos.append(nombre)
    _guardar_campos_unicos(campos_unicos)

    registrar_evento(
        accion="Restauración",
        entidad="campo_unico",
        antes={
            "campo": nombre,
            "unico": False
        },
        despues={
            "campo": nombre,
            "unico": True,
            "conflictivo": bool(conflictos)
        }
    )

    return True, {
        "campo": nombre,
        "unico": True,
        "conflictos": conflictos
    }
