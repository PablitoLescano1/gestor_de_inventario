from datetime import datetime


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

        positivos = {'si', 'sí', 's', 'true', '1', 'verdadero', 'y', 'yes', 't'}
        negativos = {'no', 'n', '0', 'false', 'falso', 'f'}

        if valor in positivos:
            return True
        if valor in negativos:
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
            return float(str(dato).strip())
        except (ValueError, TypeError):
            return None

    # FECHA
    if tipo_esperado == "fecha":
        try:
            dato = str(dato).strip()
            datetime.strptime(dato, "%d-%m-%Y")
            return dato
        except (ValueError, TypeError):
            return None

    return None
