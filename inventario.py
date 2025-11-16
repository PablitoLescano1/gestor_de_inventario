# Sistema de Inventario
# Autor: Stéfano Bertone

print('\nGESTOR DE INVENTARIO\n')

inventario = []


# MENÚ PRINCIPAL
def mostrar_menu():
    """Menú principal del sistema."""
    
    print('Menú principal:\n')
    print('1. Agregar producto.')
    print('2. Mostrar inventario.')
    print('3. Modificar producto.')
    print('4. Eliminar producto.')
    print('5. Salir.\n')


# BÚSQUEDA DE PRODUCTO EN EL INVENTARIO
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


def agregar_producto(inventario):
    """Agrega un producto nuevo o suma la cantidad si ya existe.""" 
    
    print('Agregando producto:\n')

    nombre = input('Ingrese el nombre del producto: ').strip().title()
    precio = pedir_flotante('Ingrese el precio del producto: ')
    cantidad = pedir_entero('Ingrese la cantidad del producto: ')

    p = buscar_producto(nombre, inventario)

    if (precio >= 0) and (cantidad >= 0):
        
        if p:
            print(f'El producto "{nombre}" ya existe en el inventario.')
            print(f'{p["nombre"]} | Precio: ${p["precio"]:.2f} | Cantidad: {p["cantidad"]}')

            if preguntar_si_no('¿Desea sumar la cantidad ingresada al producto existente? (si/no): '):
                p['cantidad'] += cantidad
                print('La cantidad se sumó correctamente.\n')

            else:
                print('No se sumó la cantidad y no se agregó un producto nuevo.\n')
        
        else:
            producto = {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
            inventario.append(producto)
            print('Producto agregado correctamente.\n')
            
    elif (precio < 0) or (cantidad < 0):
        
        if precio < 0:
            print('El precio no puede ser un número negativo.')
        
        if cantidad < 0:
            print('La cantidad no debería ser un número negativo.')


def mostrar_inventario(inventario):
    """Muestra los productos del inventario."""
    
    print('Mostrando inventario:\n')

    if len(inventario) == 0:
        print('No hay productos registrados.\n')
        return

    for p in inventario:
        print(f"{p['nombre']} | Precio: ${p['precio']:.2f} | Cantidad: {p['cantidad']}")
    print()


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
                nuevo_nombre = input(f'Nuevo nombre para "{p["nombre"]}": ')
                p['nombre'] = nuevo_nombre.strip().title()

            elif cambio == 2:
                nuevo_precio = pedir_flotante(f'Nuevo precio (actual ${p["precio"]:.2f}): ')
                if nuevo_precio >= 0:
                    p['precio'] = nuevo_precio
                else:
                    print('El precio debe ser un número positivo.')

            elif cambio == 3:
                nueva_cantidad = pedir_entero(f'Nueva cantidad (actual {p["cantidad"]}): ')
                if nueva_cantidad >= 0:
                    p['cantidad'] = nueva_cantidad
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

    producto = input('¿Qué producto desea eliminar?: ').strip().title()
    p = buscar_producto(producto, inventario)

    if p:
        print(f"\nNombre: {p['nombre']}\nPrecio: ${p['precio']:.2f}\nCantidad: {p['cantidad']}\n")

        if preguntar_si_no('¿Desea eliminar este producto? (si/no): '):
            inventario.remove(p)
            print('El producto se eliminó correctamente.\n')

        else:
            print('El producto no será eliminado.\n')


# BUCLE PRINCIPAL
while True:
    mostrar_menu()
    eleccion = pedir_entero('Ingrese el número de la opción deseada: ')
    print()

    if eleccion == 1:
        agregar_producto(inventario)

    elif eleccion == 2:
        mostrar_inventario(inventario)

    elif eleccion == 3:
        modificar_producto(inventario)

    elif eleccion == 4:
        eliminar_producto(inventario)

    elif eleccion == 5:
        print('\nHasta luego.\n')
        break

    else:
        print('\nOpción no válida. Intente nuevamente.\n')