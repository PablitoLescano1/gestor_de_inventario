import json

def cargar_campos():
    """Carga los campos definidos por el usuario desde campos.json"""

    try:
        with open("campos.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}


def guardar_campos(campos):
    """Guarda los campos definidos por el usuario en campos.json"""
    with open("campos.json", "w", encoding="utf-8") as archivo:
        json.dump(campos, archivo, indent=4, ensure_ascii=False)


campos = cargar_campos()


def cargar_inventario():
    """Carga el archivo .JSON"""
    try:
        with open("inventario.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


def guardar_inventario(inventario):
    """Guarda en el archivo .JSON"""
    with open("inventario.json", "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


inventario = cargar_inventario()


def producto_duplicado(nuevo, inventario):
    """Devuelve True si existe un producto idéntico en todos los campos."""
    for p in inventario:
        if p == nuevo:
            return True
    return False


def buscar_producto(nombre, inventario):
    """Busca un producto por nombre y devuelve el diccionario si existe."""
    
    for p in inventario:
        if p['nombre'].lower() == nombre.lower():
            return p
    return None


def validar_dato(mensaje, tipo_esperado):
    """Valida que los datos sean del tipo correcto"""

    while True:
        dato = input(mensaje)

        if tipo_esperado == str:
            if not dato.strip():
                print('Error: ingrese un nombre válido.')
                continue
            return dato
        
        if tipo_esperado == bool:
            if dato.strip().lower() in ['si', 'sí', 's', '1', 'true', 'verdadero', 't', 'y', 'yes']:
                return True
            elif dato.strip().lower() in ['no', 'n', '0', 'false', 'falso', 'f']:
                return False
            else:
                print('Error: ingrese un booleano válido.')
                continue
        
        if tipo_esperado == int:
            try:
                return int(dato)
            except ValueError:
                print('Error: ingrese un numero valido')
                continue
            
        if tipo_esperado == float:
            try:
                return float(dato)
            except ValueError:
                print("Error: ingrese un número válido.")
                continue
            

    """Pide un nombre valido(no vacio) y lo devuelve formateado."""

    while True:
        nombre = input(mensaje).strip()
        if not nombre:
            print('Error: ingrese un nombre válido.')
            continue
        else:
            return nombre
    

def crear_campo(campos):
    """Crea campos a eleccion del usuario"""

    campo = pedir_nombre('Ingrese el nombre del campo que desea agregar: ')
    if campo in campos:
        print(f'El campo {campo} ya existe en los campos actuales.')
        return

    print("Tipos de datos posibles: texto, num entero, num decimal, V/F, fecha")
    tipo = input(f'Ingrese el tipo de dato para "{campo}": ').strip().lower()

    if tipo not in ('texto', 'num entero', 'num decimal', 'V/F', 'fecha'):
        print("Tipo no válido. Se asigna 'texto' por defecto.")
        tipo = 'string'

    campos[campo] = tipo
    guardar_campos(campos)
    print(f'Campo "{campo}" agregado correctamente con tipo "{tipo}".')


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
            tipo_python = str
        else:
            tipo_python = str

        dato = validar_dato(f'Ingrese el valor de {campo}: ', tipo_python)
        nuevo_producto[campo] = dato

    if producto_duplicado(nuevo_producto, inventario):
        print("\nAdvertencia: este producto ya existe con todos los campos idénticos.")
        decision = validar_dato("¿Desea añadirlo igual? (si/no): ", bool)

        if not decision:
            print("Operación cancelada.\n")
            return

    inventario.append(nuevo_producto)
    guardar_inventario(inventario)

    print("Producto agregado correctamente.\n")


def mostrar_inventario(inventario):
    """Muestra los productos del inventario."""
    
    print('Mostrando inventario:\n')

    if len(inventario) == 0:
        print('No hay productos registrados.\n')
        return
    
    print('1. A-Z')
    print('2. Z-A')
    print('3. Precio menor a mayor')
    print('4. Precio mayor a menor')
    print('5. Cantidad menor a mayor')
    print('6. Cantidad mayor a menor\n')

    orden_productos = validar_dato('Ingrese el orden que desea: ', int)

    if orden_productos == 1:
        for p in sorted(inventario, key=lambda p: p['nombre']):
            print(f"{p['nombre']} | Precio: ${p['precio']:.2f} | Cantidad: {p['cantidad']}")
        print()

    elif orden_productos == 2:
        for p in sorted(inventario, key=lambda p: p['nombre'], reverse=True):
            print(f"{p['nombre']} | Precio: ${p['precio']:.2f} | Cantidad: {p['cantidad']}")
        print()

    elif orden_productos == 3:
        for p in sorted(inventario, key=lambda p: p['precio']):
            print(f"{p['nombre']} | Precio: ${p['precio']:.2f} | Cantidad: {p['cantidad']}")
        print()
    
    elif orden_productos == 4:
        for p in sorted(inventario, key=lambda p: p['precio'], reverse=True):
            print(f"{p['nombre']} | Precio: ${p['precio']:.2f} | Cantidad: {p['cantidad']}")
        print()
    
    elif orden_productos == 5:
        for p in sorted(inventario, key=lambda p: p['cantidad']):
            print(f"{p['nombre']} | Precio: ${p['precio']:.2f} | Cantidad: {p['cantidad']}")
        print()
    
    elif orden_productos == 6:
        for p in sorted(inventario, key=lambda p: p['cantidad'], reverse=True):
            print(f"{p['nombre']} | Precio: ${p['precio']:.2f} | Cantidad: {p['cantidad']}")
        print()
    
    else:
        print('Opción no válida.\n')


def modificar_producto(inventario):
    """Permite modificar el nombre, el precio o la cantidad de un producto.""" 
    
    print('Modificando producto:\n')

    producto = input('¿Qué producto desea modificar?: ').strip().title()
    p = buscar_producto(producto, inventario)

    if p:
        print(f'\nNombre: {p["nombre"]}\nPrecio: ${p["precio"]:.2f}\nCantidad: {p["cantidad"]}\n')

        while True:
            print('Datos disponibles para modificar:')
            print('1. Nombre')
            print('2. Precio')
            print('3. Cantidad')
            print('4. Salir\n')

            cambio = validar_dato('¿Qué dato desea modificar?: ', int)

            if cambio == 1:
                nuevo_nombre = validar_dato(f'Nuevo nombre para "{p["nombre"]}": ', str)
                existe = buscar_producto(nuevo_nombre, inventario)

                if existe and existe is not p:
                    print(f'Ya existe un producto con el nombre "{nuevo_nombre}".\n')
                    print('El nombre no ha cambiado.')

                elif existe is p:
                    print('El nombre ingresado es igual al actual. No se realizaron cambios.\n')

                else:
                    p['nombre'] = nuevo_nombre.strip().title()
                    guardar_inventario(inventario)
                    print("Nombre actualizado correctamente.\n")


            elif cambio == 2:
                nuevo_precio = validar_dato(f'Nuevo precio (actual ${p["precio"]:.2f}): ', float)
                if nuevo_precio >= 0:
                    p['precio'] = nuevo_precio
                    guardar_inventario(inventario)
                    print('Precio actualizado correctamente.\n')
                else:
                    print('El precio debe ser un número positivo.')

            elif cambio == 3:
                nueva_cantidad = validar_dato(f'Nueva cantidad (actual {p["cantidad"]}): ', int)
                if nueva_cantidad >= 0:
                    p['cantidad'] = nueva_cantidad
                    guardar_inventario(inventario)
                    print('Cantidad actualizada correctamente.\n')
                else:
                    print('La cantidad debe ser un número positivo.')

            elif cambio == 4:
                break

            else:
                print('Opción no válida.\n')
    
    else:
        print(f'El producto "{producto}" no existe en el inventario.\n')


def eliminar_producto(inventario):
    """Elimina un producto del inventario si existe."""
    
    print('Eliminando producto:\n')

    producto = validar_dato('¿Qué producto desea eliminar?: ', str)
    p = buscar_producto(producto, inventario)

    if p:
        print(f"\nNombre: {p['nombre']}\nPrecio: ${p['precio']:.2f}\nCantidad: {p['cantidad']}\n")

        if validar_dato('¿Desea eliminar este producto? (si/no): ', bool):
            inventario.remove(p)
            guardar_inventario(inventario)
            print('El producto se eliminó correctamente.\n')

        else:
            print('El producto no será eliminado.\n')