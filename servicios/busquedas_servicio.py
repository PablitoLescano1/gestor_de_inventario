from servicios.almacenamiento import cargar_inventario
from servicios.campo_servicio import cargar_campos
from servicios.campo_unico_servicio import es_campo_unico


def producto_duplicado(nuevo, inventario=None):
    """Devuelve True si existe un producto estrictamente idéntico en el inventario."""

    if not isinstance(nuevo, dict):
        return False

    if inventario is None:
        inventario = cargar_inventario()

    return any(producto == nuevo for producto in inventario)


def buscar_producto(valor_busqueda, campo_clave, inventario=None):
    """Busca productos cuyo valor en 'campo_clave' coincida parcial o totalmente con 'valor_busqueda'."""

    campos = cargar_campos()
    if campo_clave not in campos:
        return []

    if inventario is None:
        inventario = cargar_inventario()

    valor_busqueda = str(valor_busqueda).lower().strip()
    resultados = []

    for producto in inventario:
        valor_producto = producto.get(campo_clave)

        if valor_producto is None:
            continue

        if valor_busqueda in str(valor_producto).lower():
            resultados.append(producto)

    return resultados


def buscar_similares(criterios, inventario=None):
    """Devuelve productos que coinciden parcialmente con TODOS los criterios."""

    if not isinstance(criterios, dict) or not criterios:
        return []

    campos = cargar_campos()
    for campo in criterios:
        if campo not in campos:
            return []

    if inventario is None:
        inventario = cargar_inventario()

    resultados = []

    for producto in inventario:
        for campo, valor in criterios.items():
            valor_producto = producto.get(campo)

            if valor_producto is None:
                break

            if str(valor).lower().strip() not in str(valor_producto).lower():
                break
        else:
            resultados.append(producto)

    return resultados


def buscar_por_campo_unico(campo, valor, inventario=None):
    """Busca un producto por un campo marcado como único."""

    if not es_campo_unico(campo):
        return None

    if inventario is None:
        inventario = cargar_inventario()

    for producto in inventario:
        if producto.get(campo) == valor:
            return producto

    return None
