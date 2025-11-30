class Producto:
    def __init__(self, datos: dict):
        # datos es el dict con las claves definidas en campos.json
        self.datos = datos

    def get(self, clave, default=None):
        return self.datos.get(clave, default)

    def set(self, clave, valor):
        self.datos[clave] = valor