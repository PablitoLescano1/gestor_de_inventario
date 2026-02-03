def normalizar_nombre(nombre):
    """Normaliza nombres para uso consistente en todo el sistema.

    - Elimina espacios extra
    - Convierte valores inválidos en None
    - Garantiza strings no vacíos
    """

    if not isinstance(nombre, str):
        return None

    nombre = " ".join(nombre.strip().split())
    return nombre if nombre else None