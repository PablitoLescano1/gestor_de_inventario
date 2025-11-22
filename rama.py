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


def buscar_producto(nombre, inventario):
    """Busca un producto por nombre y devuelve el diccionario si existe."""
    
    for p in inventario:
        if p['nombre'].lower() == nombre.lower():
            return p
    return None


def pedir_entero(mensaje):
    """Valida la entrada de un número entero."""
    
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: ingrese un número entero válido.")


def pedir_flotante(mensaje):
    """Valida la entrada de un número flotante."""
    
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: ingrese un número válido.")


def preguntar_si_no(mensaje):
    """Solicita una respuesta sí/no y devuelve True o False."""
    
    while True:
        r = input(mensaje).strip().lower()
        if r in ('si', 'sí', 's'):
            return True
        if r in ('no', 'n'):
            return False
        print("Opción no válida. Responda «sí» o «no».")


def pedir_nombre(mensaje):
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

    print("Tipos de datos posibles: string, int, float, boolean, date")
    tipo = input(f'Ingrese el tipo de dato para "{campo}": ').strip().lower()

    if tipo not in ('string', 'int', 'float', 'boolean', 'date'):
        print("Tipo no válido. Se asigna 'string' por defecto.")
        tipo = 'string'

    campos[campo] = tipo
    guardar_campos(campos)
    print(f'Campo "{campo}" agregado correctamente con tipo "{tipo}".')


def agregar_producto(inventario):
    """Agrega un producto nuevo o suma la cantidad si ya existe.""" 
    
    print('Agregando producto:\n')

    for campo in campos:
        


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

    orden_productos = pedir_entero('Ingrese el orden que desea: ')

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

            cambio = pedir_entero('¿Qué dato desea modificar?: ')

            if cambio == 1:
                nuevo_nombre = pedir_nombre(f'Nuevo nombre para "{p["nombre"]}": ')
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
                nuevo_precio = pedir_flotante(f'Nuevo precio (actual ${p["precio"]:.2f}): ')
                if nuevo_precio >= 0:
                    p['precio'] = nuevo_precio
                    guardar_inventario(inventario)
                    print('Precio actualizado correctamente.\n')
                else:
                    print('El precio debe ser un número positivo.')

            elif cambio == 3:
                nueva_cantidad = pedir_entero(f'Nueva cantidad (actual {p["cantidad"]}): ')
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

    producto = pedir_nombre('¿Qué producto desea eliminar?: ')
    p = buscar_producto(producto, inventario)

    if p:
        print(f"\nNombre: {p['nombre']}\nPrecio: ${p['precio']:.2f}\nCantidad: {p['cantidad']}\n")

        if preguntar_si_no('¿Desea eliminar este producto? (si/no): '):
            inventario.remove(p)
            guardar_inventario(inventario)
            print('El producto se eliminó correctamente.\n')

        else:
            print('El producto no será eliminado.\n')