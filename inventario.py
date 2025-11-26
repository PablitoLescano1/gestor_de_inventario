import json
from datetime import datetime


def cargar_campos():
    """Carga los campos definidos por el usuario desde campos.json."""
    
    try:
        with open("campos.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}


def guardar_campos(campos):
    """Guarda los campos definidos por el usuario en campos.json."""
    
    with open("campos.json", "w", encoding="utf-8") as archivo:
        json.dump(campos, archivo, indent=4, ensure_ascii=False)


campos = cargar_campos()


def cargar_inventario():
    """Carga el archivo inventario.json y devuelve la lista de productos."""
    
    try:
        with open("inventario.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


def guardar_inventario(inventario):
    """Guarda la lista de productos en inventario.json."""
    
    with open("inventario.json", "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


inventario = cargar_inventario()


def producto_duplicado(nuevo, inventario):
    """Devuelve True si existe un producto idéntico (mismo dict) en el inventario."""
    
    for p in inventario:
        if p == nuevo:
            return True
    return False


def buscar_producto(campo, valor, inventario):
    """Busca un producto por cualquier campo definido en 'campos'.
    Devuelve el primer producto que coincida o None."""
    
    if campo not in campos:
        print(f'El campo "{campo}" no existe.')
        return None

    for p in inventario:
        val = p.get(campo)
        if isinstance(val, str) and isinstance(valor, str):
            if val.lower() == valor.lower():
                return p
        else:
            if val == valor:
                return p
            
    return None


def validar_dato(mensaje, tipo_esperado):
    """Valida que los datos sean del tipo correcto: str, int, float, bool, 'fecha'."""
    
    while True:
        dato = input(mensaje).strip()

        if tipo_esperado == str:
            if not dato:
                print("Error: ingrese un texto válido.")
                continue
            return dato

        elif tipo_esperado == bool:
            if dato.lower() in ['si', 'sí', 's', '1', 'true', 'verdadero', 't', 'y', 'yes']:
                return True
            elif dato.lower() in ['no', 'n', '0', 'false', 'falso', 'f']:
                return False
            else:
                print("Error: ingrese 'si' o 'no'.")
                continue

        elif tipo_esperado == int:
            try:
                return int(dato)
            except ValueError:
                print("Error: ingrese un número entero válido.")
                continue

        elif tipo_esperado == float:
            try:
                return float(dato)
            except ValueError:
                print("Error: ingrese un número decimal válido.")
                continue

        elif tipo_esperado == 'fecha':
            try:
                datetime.strptime(dato, '%d-%m-%Y')
                return dato
            except ValueError:
                print("Error: ingrese fecha DD-MM-AAAA.")
                continue

        else:
            if dato:
                return dato
            print("Error: ingrese un valor válido.")
            continue


def crear_campo(campos):
    """Crea un campo nuevo en el diccionario de campos."""
    
    campo = validar_dato('Ingrese el nombre del campo que desea agregar: ', str)
    if campo in campos:
        print(f'El campo "{campo}" ya existe.')
        return

    print("Tipos: texto, num entero, num decimal, v/f, fecha")
    tipo = input(f'Tipo de dato para \"{campo}\": ').strip().lower()

    if tipo not in ('texto', 'num entero', 'num decimal', 'v/f', 'fecha'):
        print("Tipo no válido. Se asigna 'texto'.")
        tipo = 'texto'

    campos[campo] = tipo
    guardar_campos(campos)
    print(f'Campo "{campo}" agregado correctamente.')


def agregar_producto(inventario):
    """Agrega un producto nuevo verificando duplicados."""
    
    print('Agregando producto:\n')
    nuevo_producto = {}

    for campo in campos:
        tipo_logico = campos[campo]

        if tipo_logico == 'texto':
            tipo_python = str
        elif tipo_logico == 'num entero':
            tipo_python = int
        elif tipo_logico == 'num decimal':
            tipo_python = float
        elif tipo_logico == 'v/f':
            tipo_python = bool
        elif tipo_logico == 'fecha':
            tipo_python = 'fecha'
        else:
            tipo_python = str

        dato = validar_dato(f'Ingrese el valor de {campo}: ', tipo_python)
        nuevo_producto[campo] = dato

    if producto_duplicado(nuevo_producto, inventario):
        print("\nAdvertencia: este producto ya existe.")
        decision = validar_dato("¿Desea añadirlo igual? (si/no): ", bool)
        if not decision:
            print("Operación cancelada.\n")
            return

    inventario.append(nuevo_producto)
    guardar_inventario(inventario)
    print("Producto agregado correctamente.\n")


def ordenar_y_mostrar(inventario):
    """Permite elegir un campo y ordenar ascendente o descendente."""

    lista_campos = list(campos.keys())

    print("\nCampos disponibles para ordenar:")
    for i, campo in enumerate(lista_campos, start=1):
        print(f"{i}. {campo}")

    while True:
        indice = validar_dato("\n¿Por cuál campo desea ordenar?: ", int)
        if 1 <= indice <= len(lista_campos):
            campo_elegido = lista_campos[indice - 1]
            break
        print("Opción inválida.")

    print("\n1. Ascendente")
    print("2. Descendente")
    while True:
        modo = validar_dato("¿En cuál orden?: ", int)
        if modo == 1:
            reverse = False
            break
        elif modo == 2:
            reverse = True
            break
        print("Opción inválida.")

    def clave(item):
        valor = item.get(campo_elegido)
        if valor is None:
            tipo = campos[campo_elegido]
            if tipo in ('num entero', 'num decimal'):
                return 0
            return ""  
        
        if campos[campo_elegido] == 'fecha':
            try:
                return datetime.strptime(valor, '%d-%m-%Y')
            except:
                return valor
        return valor

    inventario_ordenado = sorted(inventario, key=clave, reverse=reverse)
    mostrar_inventario(inventario_ordenado)


def mostrar_inventario(inventario):
    """Muestra los productos según el orden de los campos."""
    
    if not inventario:
        print('No hay productos registrados.\n')
        return

    for c in campos:
        print(c, end=' | ')
    print()

    for p in inventario:
        for c in campos:
            valor = p.get(c, '-')
            if isinstance(valor, bool):
                valor = 'Sí' if valor else 'No'
            print(valor, end=' | ')
        print()
    print()


def modificar_producto(inventario):
    print("Función modificar_producto aún no implementada.\n")


def eliminar_producto(inventario):
    print("Función eliminar_producto aún no implementada.\n")