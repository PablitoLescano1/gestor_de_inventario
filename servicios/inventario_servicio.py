import json

from almacenamiento import RUTA_INVENTARIO
from campo_servicio import cargar_campos
from campo_unico_servicio import es_campo_unico
from validadores import validar_dato
from busquedas_servicio import buscar_similares
from historial_servicio import registrar_evento


def cargar_inventario():
    """Carga el archivo inventario.json y devuelve la lista de productos."""
    
    try:
        with open(RUTA_INVENTARIO, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_inventario(inventario):
    """Guarda la lista de productos en inventario.json."""
    
    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


def __validar_unicidad(nuevo_producto, inventario):
    """Verifica que los campos únicos no tengan valores duplicados."""
    
    for campo, valor in nuevo_producto.items():
        if not es_campo_unico(campo):
            continue

        for prod in inventario:
            if prod.get(campo) == valor:
                return False, (
                    f"El campo único '{campo}' no puede repetir el valor '{valor}'."
                )

    return True, None


def agregar_producto(datos, criterios=None, forzar_agregar=False):
    """Agrega un producto validando tipos, duplicados y campos únicos."""

    if not isinstance(datos, dict):
        return False, "Los datos del producto deben enviarse como diccionario."

    campos = cargar_campos()
    inventario = cargar_inventario()

    tipo_map = {
        "texto": str,
        "num entero": int,
        "num decimal": float,
        "v/f": bool,
        "fecha": "fecha"
    }

    nuevo_producto = {}

    for campo, tipo_logico in campos.items():
        if campo not in datos:
            return False, f"Falta el campo '{campo}'."

        tipo_py = tipo_map[tipo_logico]
        valor = validar_dato(datos[campo], tipo_py)

        if valor is None:
            return False, f"Valor inválido para el campo '{campo}'."

        nuevo_producto[campo] = valor

    ok, err = __validar_unicidad(nuevo_producto, inventario)
    if not ok:
        return False, err

    if criterios is None:
        criterios = nuevo_producto.copy()

    duplicados = buscar_similares(criterios)
    if duplicados and not forzar_agregar:
        return False, duplicados

    inventario.append(nuevo_producto)
    guardar_inventario(inventario)

    # Historial: alta de producto
    registrar_evento(
        accion="Alta",
        entidad="producto",
        antes=None,
        despues=nuevo_producto.copy()
    )

    return True, nuevo_producto.copy()


def modificar_producto(criterios, nuevos_datos):
    """Modifica un producto usando criterios de búsqueda."""

    if not isinstance(criterios, dict) or not criterios:
        return False, "Los criterios deben ser un diccionario no vacío."

    if not isinstance(nuevos_datos, dict) or not nuevos_datos:
        return False, "Los nuevos datos deben ser un diccionario no vacío."

    campos = cargar_campos()
    inventario = cargar_inventario()

    coincidencias = buscar_similares(criterios)
    if not coincidencias:
        return False, "No se encontraron productos que coincidan."

    if len(coincidencias) > 1:
        return None, coincidencias.copy()

    producto = coincidencias[0]
    estado_anterior = producto.copy()

    tipo_map = {
        "texto": str,
        "num entero": int,
        "num decimal": float,
        "v/f": bool,
        "fecha": "fecha"
    }

    producto_modificado = producto.copy()

    for campo, valor_raw in nuevos_datos.items():
        if campo not in campos:
            return False, f"El campo '{campo}' no existe."

        tipo_py = tipo_map[campos[campo]]
        valor = validar_dato(valor_raw, tipo_py)

        if valor is None:
            return False, f"Valor inválido para el campo '{campo}'."

        producto_modificado[campo] = valor

    otros = [p for p in inventario if p is not producto]
    ok, err = __validar_unicidad(producto_modificado, otros)
    if not ok:
        return False, err

    producto.update(producto_modificado)
    guardar_inventario(inventario)

    # Historial: modificación de producto
    registrar_evento(
        accion="Modificación",
        entidad="producto",
        antes=estado_anterior,
        despues=producto.copy()
    )

    return True, producto.copy()


def eliminar_producto(criterios, producto_elegido=None):
    """Elimina un producto usando criterios de búsqueda."""

    if not isinstance(criterios, dict) or not criterios:
        return False, "Los criterios deben ser un diccionario no vacío."

    inventario = cargar_inventario()
    coincidencias = buscar_similares(criterios)

    if not coincidencias:
        return False, "No se encontraron productos que coincidan."

    if producto_elegido is None:
        if len(coincidencias) == 1:
            producto = coincidencias[0]
        else:
            return None, coincidencias.copy()
    else:
        if producto_elegido not in inventario:
            return False, "El producto elegido no existe."
        producto = producto_elegido

    estado_anterior = producto.copy()
    inventario.remove(producto)
    guardar_inventario(inventario)

    # Historial: eliminación de producto
    registrar_evento(
        accion="Eliminación",
        entidad="producto",
        antes=estado_anterior,
        despues=None
    )

    return True, estado_anterior
