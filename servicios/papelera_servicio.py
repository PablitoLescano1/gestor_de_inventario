import uuid
from datetime import datetime, timedelta

from servicios.almacenamiento import (
    cargar_papelera,
    guardar_papelera
)


TTL_DIAS = 30


def _ahora():
    """Devuelve la fecha y hora actual."""
    return datetime.now()


def limpiar_expirados():
    """Elimina definitivamente los registros de papelera expirados."""

    papelera = cargar_papelera()
    ahora = _ahora()

    papelera_vigente = [
        r for r in papelera
        if datetime.fromisoformat(r["expira_en"]) > ahora
    ]

    guardar_papelera(papelera_vigente)
    return True


def enviar_a_papelera(entidad, snapshot, schema_snapshot=None, motivo=None, meta=None):
    """Envía una entidad a la papelera con su estado completo."""

    ahora = _ahora()

    registro = {
        "id": str(uuid.uuid4()),
        "entidad": entidad,
        "snapshot": snapshot,
        "schema_snapshot": schema_snapshot,
        "motivo": motivo,
        "meta": meta or {},
        "fecha_eliminacion": ahora.isoformat(),
        "expira_en": (ahora + timedelta(days=TTL_DIAS)).isoformat()
    }

    papelera = cargar_papelera()
    papelera.append(registro)
    guardar_papelera(papelera)

    return registro


def listar_papelera(entidad=None, incluir_expirados=False):
    """Lista los registros de la papelera."""

    papelera = cargar_papelera()
    ahora = _ahora()

    resultados = []

    for r in papelera:
        if not incluir_expirados:
            if datetime.fromisoformat(r["expira_en"]) <= ahora:
                continue

        if entidad and r["entidad"] != entidad:
            continue

        resultados.append(r.copy())

    return resultados


def obtener_registro(registro_id):
    """Obtiene un registro específico por ID."""

    papelera = cargar_papelera()

    for r in papelera:
        if r["id"] == registro_id:
            return r.copy()

    return None


def restaurar_registro(registro_id):
    """Restaura un registro de la papelera."""

    papelera = cargar_papelera()
    ahora = _ahora()

    for i, r in enumerate(papelera):
        if r["id"] != registro_id:
            continue

        if datetime.fromisoformat(r["expira_en"]) <= ahora:
            return False, "El registro ha expirado y no puede restaurarse."

        registro = papelera.pop(i)
        guardar_papelera(papelera)

        advertencias = []

        if registro.get("schema_snapshot"):
            advertencias.append(
                "El registro fue restaurado con su esquema original. "
                "Algunos campos pueden no existir actualmente."
            )

        return True, {
            "entidad": registro["entidad"],
            "snapshot": registro["snapshot"],
            "schema_snapshot": registro.get("schema_snapshot"),
            "advertencias": advertencias
        }

    return False, "Registro no encontrado en la papelera."


def detectar_conflictos_restauracion(registro, inventario_actual, campos_actuales, campos_unicos):
    """Analiza si un registro restaurado generaría conflictos con el estado actual del sistema."""

    conflictos = []
    snapshot = registro.get("snapshot", {})

    # Conflictos por campos únicos
    for campo in campos_unicos:
        if campo not in snapshot:
            continue

        valor = snapshot[campo]

        for producto in inventario_actual:
            if producto.get(campo) == valor:
                conflictos.append({
                    "tipo": "campo_unico",
                    "campo": campo,
                    "valor": valor,
                    "descripcion": (
                        f"El valor '{valor}' ya existe en otro producto "
                        f"para el campo único '{campo}'."
                    )
                })
                break

    # Campos que ya no existen
    for campo in snapshot:
        if campo not in campos_actuales:
            conflictos.append({
                "tipo": "campo_inexistente",
                "campo": campo,
                "valor": snapshot[campo],
                "descripcion": (
                    f"El campo '{campo}' ya no existe en el sistema."
                )
            })

    return conflictos
