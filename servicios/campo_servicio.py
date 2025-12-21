import json

from almacenamiento import RUTA_CAMPOS
from campo_unico_servicio import (
    marcar_campo_unico,
    es_campo_unico,
    desmarcar_campo_unico
)
from inventario_servicio import cargar_inventario, guardar_inventario
from papelera_servicio import enviar_a_papelera
from historial_servicio import registrar_evento


def _normalizar_nombre(nombre):
    """Normaliza nombres de campo para uso interno consistente."""
    
    if not isinstance(nombre, str):
        return None
    return " ".join(nombre.strip().split())


def cargar_campos():
    """Carga los campos definidos por el usuario."""
    
    try:
        with open(RUTA_CAMPOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return {}
            return json.loads(contenido)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def guardar_campos(campos):
    """Guarda los campos definidos por el usuario."""
    
    with open(RUTA_CAMPOS, "w", encoding="utf-8") as archivo:
        json.dump(campos, archivo, indent=4, ensure_ascii=False)


def crear_campo(nombre, tipo, es_unico=False):
    """Crea un campo nuevo en el sistema."""

    campos = cargar_campos()

    nombre = _normalizar_nombre(nombre)
    if not nombre:
        return False, "Nombre inválido."

    tipo = tipo.strip().lower()
    tipos_validos = ("texto", "num entero", "num decimal", "v/f", "fecha")

    if tipo not in tipos_validos:
        return False, "Tipo inválido."

    if nombre in campos:
        return False, "El campo ya existe."

    campos[nombre] = tipo
    guardar_campos(campos)

    if es_unico:
        marcar_campo_unico(nombre)

    registrar_evento(
        accion="Alta",
        entidad="campo",
        antes=None,
        despues={
            "nombre": nombre,
            "tipo": tipo,
            "unico": es_unico
        }
    )

    return True, None


def eliminar_campo(nombre_campo):
    """Elimina un campo del sistema de forma no destructiva."""

    nombre_campo = _normalizar_nombre(nombre_campo)
    if not nombre_campo:
        return False, "Nombre inválido."

    campos = cargar_campos()
    inventario = cargar_inventario()

    if nombre_campo not in campos:
        return False, "El campo no existe."

    if len(campos) == 1:
        return False, "No se puede eliminar el último campo."

    snapshot = {
        "nombre": nombre_campo,
        "tipo": campos[nombre_campo],
        "unico": es_campo_unico(nombre_campo),
        "valores_por_producto": {}
    }

    for idx, producto in enumerate(inventario):
        if nombre_campo in producto:
            snapshot["valores_por_producto"][idx] = producto[nombre_campo]

            producto.setdefault("_campos_ocultos", {})
            producto["_campos_ocultos"][nombre_campo] = producto[nombre_campo]
            del producto[nombre_campo]

    enviar_a_papelera(
        entidad="campo",
        snapshot=snapshot,
        schema_snapshot={
            "nombre": nombre_campo,
            "tipo": campos[nombre_campo],
            "unico": es_campo_unico(nombre_campo)
        },
        motivo="eliminacion_campo"
    )

    del campos[nombre_campo]

    if es_campo_unico(nombre_campo):
        desmarcar_campo_unico(nombre_campo)

    guardar_campos(campos)
    guardar_inventario(inventario)

    registrar_evento(
        accion="Eliminación",
        entidad="campo",
        antes=snapshot,
        despues=None
    )

    return True, None
