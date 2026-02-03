import json

from almacenamiento import RUTA_INVENTARIO

# Servicios de dominio
from campo_servicio import cargar_campos
from campo_unico_servicio import validar_unicidad_producto
from busquedas_servicio import buscar_similares
from historial_servicio import registrar_evento
from papelera_servicio import enviar_a_papelera, restaurar_registro

# Validaciones
from validadores import validar_dato


def cargar_inventario():
    """Carga el archivo inventario.json y devuelve la lista de productos."""

    try:
        with open(RUTA_INVENTARIO, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            return json.loads(contenido) if contenido else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_inventario(inventario):
    """Guarda la lista de productos en inventario.json."""

    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


def agregar_producto(datos, criterios=None, forzar_agregar=False):
    """Agrega un producto validando tipos, duplicados y unicidad."""

    if not isinstance(datos, dict):
        return False, "Los datos deben ser un diccionario."

    campos = cargar_campos()
    inventario = cargar_inventario()

    tipo_map = {
        "texto": str,
        "num entero": int,
        "num decimal": float,
        "v/f": bool,
        "fecha": "fecha"
    }

    nuevo = {}

    for campo, tipo_logico in campos.items():
        if campo not in datos:
            return False, f"Falta el campo obligatorio '{campo}'."

        valor = validar_dato(datos[campo], tipo_map[tipo_logico])
        if valor is None:
            return False, f"Valor inválido para el campo '{campo}'."

        nuevo[campo] = valor

    conflictos = validar_unicidad_producto(nuevo, inventario)
    if conflictos:
        return False, {
            "motivo": "conflicto_unicidad",
            "conflictos": conflictos
        }

    if criterios is None:
        criterios = nuevo.copy()

    duplicados = buscar_similares(criterios)
    if duplicados and not forzar_agregar:
        return False, {
            "motivo": "posible_duplicado",
            "coincidencias": duplicados
        }

    inventario.append(nuevo)
    guardar_inventario(inventario)

    registrar_evento(
        accion="Alta",
        entidad="producto",
        antes=None,
        despues=nuevo.copy()
    )

    return True, nuevo.copy()


def eliminar_producto(criterios, producto_elegido=None):
    """Envía un producto a la papelera y lo elimina del inventario."""

    inventario = cargar_inventario()
    coincidencias = buscar_similares(criterios)

    if not coincidencias:
        return False, "No se encontraron productos."

    if producto_elegido is None:
        if len(coincidencias) > 1:
            return None, coincidencias.copy()
        producto = coincidencias[0]
    else:
        producto = producto_elegido

    snapshot = producto.copy()
    schema_snapshot = cargar_campos()

    enviar_a_papelera(
        entidad="producto",
        snapshot=snapshot,
        schema_snapshot=schema_snapshot,
        motivo="eliminacion_producto"
    )

    inventario.remove(producto)
    guardar_inventario(inventario)

    registrar_evento(
        accion="Eliminación",
        entidad="producto",
        antes=snapshot,
        despues=None
    )

    return True, snapshot


def restaurar_producto(registro_id):
    """Restaura un producto desde la papelera."""

    inventario = cargar_inventario()
    campos_actuales = cargar_campos()

    ok, resultado = restaurar_registro(registro_id)
    if not ok:
        return False, resultado

    producto = resultado["snapshot"]
    advertencias = resultado.get("advertencias", [])

    campos_inexistentes = [
        campo for campo in producto
        if campo not in campos_actuales
    ]

    if campos_inexistentes:
        advertencias.append({
            "tipo": "campos_inexistentes",
            "campos": campos_inexistentes
        })

    conflictos = validar_unicidad_producto(producto, inventario)
    if conflictos:
        return False, {
            "motivo": "conflicto_restauracion",
            "conflictos": conflictos,
            "snapshot": producto,
            "advertencias": advertencias
        }

    inventario.append(producto)
    guardar_inventario(inventario)

    registrar_evento(
        accion="Restauración",
        entidad="producto",
        antes=None,
        despues=producto.copy()
    )

    return True, {
        "producto": producto.copy(),
        "advertencias": advertencias
    }
