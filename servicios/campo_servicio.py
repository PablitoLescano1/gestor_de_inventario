import json

from almacenamiento import RUTA_CAMPOS
from campo_unico_servicio import (
    marcar_campo_unico,
    es_campo_unico,
    desmarcar_campo_unico
)
from inventario_servicio import cargar_inventario, guardar_inventario
from validadores import validar_dato
from historial_servicio import registrar_evento


def _normalizar_nombre(nombre):
    """Normaliza nombres de campo para uso interno consistente."""
    
    if not isinstance(nombre, str):
        return None
    return " ".join(nombre.strip().split())


def cargar_campos():
    """Carga los campos definidos por el usuario desde campos.json."""
    
    try:
        with open(RUTA_CAMPOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return {}
            return json.loads(contenido)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def guardar_campos(campos):
    """Guarda los campos definidos por el usuario en campos.json."""
    
    with open(RUTA_CAMPOS, "w", encoding="utf-8") as archivo:
        json.dump(campos, archivo, indent=4, ensure_ascii=False)


def crear_campo(nombre, tipo, es_unico=False):
    """Crea un campo nuevo en el sistema."""

    campos = cargar_campos()

    nombre = _normalizar_nombre(nombre)
    if not nombre:
        return False, "Nombre de campo inválido."

    tipo_normalizado = tipo.strip().lower() if isinstance(tipo, str) else ""
    tipos_validos = ("texto", "num entero", "num decimal", "v/f", "fecha")

    if tipo_normalizado not in tipos_validos:
        return False, f"Tipo inválido. Debe ser uno de: {', '.join(tipos_validos)}."

    if nombre in campos:
        return False, f'El campo "{nombre}" ya existe.'

    campos[nombre] = tipo_normalizado
    guardar_campos(campos)

    if es_unico:
        marcar_campo_unico(nombre)

    # Historial: alta de campo
    registrar_evento(
        accion="Alta",
        entidad="campo",
        antes=None,
        despues={
            "nombre": nombre,
            "tipo": tipo_normalizado,
            "unico": es_unico
        }
    )

    return True, None


def modificar_campo(nombre_actual, nuevo_nombre=None, nuevo_tipo=None):
    """Modifica un campo existente."""

    campos = cargar_campos()
    inventario = cargar_inventario()

    nombre_actual = _normalizar_nombre(nombre_actual)
    if not nombre_actual or nombre_actual not in campos:
        return False, f'El campo "{nombre_actual}" no existe.'

    if not nuevo_nombre and not nuevo_tipo:
        return False, "No se indicó ningún cambio."

    estado_anterior = {
        "nombre": nombre_actual,
        "tipo": campos[nombre_actual],
        "unico": es_campo_unico(nombre_actual)
    }

    tipo_map = {
        "texto": str,
        "num entero": int,
        "num decimal": float,
        "v/f": bool,
        "fecha": "fecha"
    }

    nombre_final = nombre_actual

    # CAMBIO DE NOMBRE
    if nuevo_nombre:
        nuevo_nombre = _normalizar_nombre(nuevo_nombre)
        if not nuevo_nombre:
            return False, "El nuevo nombre es inválido."

        if nuevo_nombre != nombre_actual and nuevo_nombre in campos:
            return False, f'Ya existe un campo llamado "{nuevo_nombre}".'

        tipo_original = campos[nombre_actual]
        del campos[nombre_actual]
        campos[nuevo_nombre] = tipo_original

        for producto in inventario:
            if nombre_actual in producto:
                producto[nuevo_nombre] = producto[nombre_actual]
                del producto[nombre_actual]

        nombre_final = nuevo_nombre

    # CAMBIO DE TIPO
    if nuevo_tipo:
        tipo_normalizado = nuevo_tipo.strip().lower()
        tipos_validos = ("texto", "num entero", "num decimal", "v/f", "fecha")

        if tipo_normalizado not in tipos_validos:
            return False, f"Tipo inválido. Debe ser uno de: {', '.join(tipos_validos)}."

        tipo_py = tipo_map[tipo_normalizado]

        for producto in inventario:
            if nombre_final not in producto:
                continue

            valor = producto[nombre_final]
            if validar_dato(str(valor), tipo_py) is None:
                return False, (
                    f"El valor '{valor}' no coincide con el tipo '{tipo_normalizado}'."
                )

        campos[nombre_final] = tipo_normalizado

    if nuevo_nombre and es_campo_unico(nombre_actual):
        desmarcar_campo_unico(nombre_actual)
        marcar_campo_unico(nombre_final)

    guardar_campos(campos)
    guardar_inventario(inventario)

    # Historial: modificación de campo
    registrar_evento(
        accion="Modificación",
        entidad="campo",
        antes=estado_anterior,
        despues={
            "nombre": nombre_final,
            "tipo": campos[nombre_final],
            "unico": es_campo_unico(nombre_final)
        }
    )

    return True, {"campo": nombre_final, "tipo": campos[nombre_final]}


def eliminar_campo(nombre_campo):
    """Elimina un campo del sistema y de todos los productos."""

    nombre_campo = _normalizar_nombre(nombre_campo)
    if not nombre_campo:
        return False, "Nombre de campo inválido."

    campos = cargar_campos()
    inventario = cargar_inventario()

    if nombre_campo not in campos:
        return False, f'El campo "{nombre_campo}" no existe.'

    if len(campos) == 1:
        return False, "No se puede eliminar el último campo del sistema."

    estado_anterior = {
        "nombre": nombre_campo,
        "tipo": campos[nombre_campo],
        "unico": es_campo_unico(nombre_campo)
    }

    del campos[nombre_campo]

    if es_campo_unico(nombre_campo):
        desmarcar_campo_unico(nombre_campo)

    for producto in inventario:
        if nombre_campo in producto:
            del producto[nombre_campo]

    guardar_campos(campos)
    guardar_inventario(inventario)

    # Historial: eliminación de campo
    registrar_evento(
        accion="Eliminación",
        entidad="campo",
        antes=estado_anterior,
        despues=None
    )

    return True, None
