from datetime import datetime


# Valores aceptados para booleanos
POSITIVOS = {'si', 'sí', 's', 'true', '1', 'verdadero', 'y', 'yes', 't'}
NEGATIVOS = {'no', 'n', '0', 'false', 'falso', 'f'}


def validar_dato(dato, tipo_esperado):
    """Valida y convierte un dato según el tipo esperado."""

    if dato is None:
        return None

    # TEXTO
    if tipo_esperado == str:
        dato = str(dato).strip()
        return dato if dato else None

    # BOOLEANO
    if tipo_esperado == bool:
        valor = str(dato).strip().lower()

        if valor in POSITIVOS:
            return True
        if valor in NEGATIVOS:
            return False

        return None

    # ENTERO
    if tipo_esperado == int:
        try:
            return int(str(dato).strip())
        except (ValueError, TypeError):
            return None

    # DECIMAL
    if tipo_esperado == float:
        try:
            dato = str(dato).strip().replace(",", ".")
            return float(dato)
        except (ValueError, TypeError):
            return None

    # FECHA (DD-MM-YYYY)
    if tipo_esperado == "fecha":
        try:
            dato = str(dato).strip()
            datetime.strptime(dato, "%d-%m-%Y")
            return dato
        except (ValueError, TypeError):
            return None

    return None
