from almacenamiento import (
    cargar_campos,
    guardar_campos,
    cargar_inventario,
    guardar_inventario,
    normalizar_nombre
)

from campo_unico_servicio import (
    marcar_campo_unico,
    desmarcar_campo_unico,
    es_campo_unico
)

from papelera_servicio import enviar_a_papelera
from historial_servicio import registrar_evento
from validadores import validar_dato


# Registro de tipos de campo y su lógica de validación/conversión
TIPOS_CAMPOS = {
    "texto": {
        "validador": lambda v: validar_dato(v, str)
    },
    "num entero": {
        "validador": lambda v: validar_dato(v, int)
    },
    "num decimal": {
        "validador": lambda v: validar_dato(v, float)
    },
    "v/f": {
        "validador": lambda v: validar_dato(v, bool)
    },
    "fecha": {
        "validador": lambda v: validar_dato(v, "fecha")
    }
}


def crear_campo(nombre, tipo, unico=False):
    """Crea un campo nuevo en el sistema."""

    campos = cargar_campos()

    nombre = normalizar_nombre(nombre)
    if not nombre:
        return False, "Nombre inválido."

    if nombre in campos:
        return False, "El campo ya existe."

    if tipo not in TIPOS_CAMPOS:
        return False, "Tipo inválido."

    campos[nombre] = tipo
    guardar_campos(campos)

    if unico:
        marcar_campo_unico(nombre)

    registrar_evento(
        accion="Alta",
        entidad="campo",
        despues={
            "nombre": nombre,
            "tipo": tipo,
            "unico": unico
        }
    )

    return True, None


def modificar_campo(nombre_actual, nuevo_nombre=None, nuevo_tipo=None, unico=None):
    """Modifica un campo existente."""

    campos = cargar_campos()
    inventario = cargar_inventario()

    nombre_actual = normalizar_nombre(nombre_actual)
    if nombre_actual not in campos:
        return False, "El campo no existe."

    # Validación de nuevo nombre
    if nuevo_nombre is not None:
        nuevo_nombre = normalizar_nombre(nuevo_nombre)
        if not nuevo_nombre:
            return False, "Nombre inválido."

        if nuevo_nombre != nombre_actual and nuevo_nombre in campos:
            return False, "Ya existe un campo con ese nombre."

    # Validación de nuevo tipo
    if nuevo_tipo is not None:
        if nuevo_tipo not in TIPOS_CAMPOS:
            return False, "Tipo inválido."

        validador = TIPOS_CAMPOS[nuevo_tipo]["validador"]

        for producto in inventario:
            if nombre_actual not in producto:
                continue

            if validador(producto[nombre_actual]) is None:
                return False, (
                    f"No se puede convertir el valor "
                    f"'{producto[nombre_actual]}' al tipo '{nuevo_tipo}'."
                )

    antes = {
        "nombre": nombre_actual,
        "tipo": campos[nombre_actual],
        "unico": es_campo_unico(nombre_actual)
    }

    nombre_final = nombre_actual

    # Cambio de nombre
    if nuevo_nombre and nuevo_nombre != nombre_actual:
        campos[nuevo_nombre] = campos.pop(nombre_actual)
        nombre_final = nuevo_nombre

        for producto in inventario:
            if nombre_actual in producto:
                producto[nuevo_nombre] = producto.pop(nombre_actual)

        if es_campo_unico(nombre_actual):
            desmarcar_campo_unico(nombre_actual)
            marcar_campo_unico(nombre_final)

    # Cambio de tipo
    if nuevo_tipo:
        campos[nombre_final] = nuevo_tipo
        validador = TIPOS_CAMPOS[nuevo_tipo]["validador"]

        for producto in inventario:
            if nombre_final in producto:
                producto[nombre_final] = validador(producto[nombre_final])

    # Cambio de unicidad
    if unico is not None:
        if unico:
            marcar_campo_unico(nombre_final)
        else:
            desmarcar_campo_unico(nombre_final)

    guardar_campos(campos)
    guardar_inventario(inventario)

    registrar_evento(
        accion="Modificación",
        entidad="campo",
        antes=antes,
        despues={
            "nombre": nombre_final,
            "tipo": campos[nombre_final],
            "unico": es_campo_unico(nombre_final)
        }
    )

    return True, None


def eliminar_campo(nombre):
    """Elimina un campo de forma no destructiva."""

    campos = cargar_campos()
    inventario = cargar_inventario()

    nombre = normalizar_nombre(nombre)
    if nombre not in campos:
        return False, "El campo no existe."

    if len(campos) == 1:
        return False, "No se puede eliminar el último campo."

    snapshot = {
        "nombre": nombre,
        "tipo": campos[nombre],
        "unico": es_campo_unico(nombre),
        "valores": {}
    }

    for i, producto in enumerate(inventario):
        if nombre in producto:
            snapshot["valores"][i] = producto[nombre]
            producto.setdefault("_campos_ocultos", {})[nombre] = producto[nombre]
            del producto[nombre]

    enviar_a_papelera(
        entidad="campo",
        snapshot=snapshot,
        motivo="eliminacion_campo"
    )

    if es_campo_unico(nombre):
        desmarcar_campo_unico(nombre)

    del campos[nombre]

    guardar_campos(campos)
    guardar_inventario(inventario)

    registrar_evento(
        accion="Eliminación",
        entidad="campo",
        antes=snapshot
    )

    return True, None
