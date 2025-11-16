# Sistema de Inventario
# Autor: Stéfano Bertone

print('\nGESTOR DE INVENTARIO\n')

inventario = []


# MENÚ PRINCIPAL
def mostrar_menu():
    """Menú principal del sistema."""
    print('Menú principal\n')
    print('1. Agregar producto')
    print('2. Mostrar inventario')
    print('3. Modificar producto')
    print('4. Eliminar producto')
    print('5. Salir\n')


# BÚSQUEDA DE PRODUCTO
def buscar_producto(nombre, inventario):
    """Busca un producto por nombre y devuelve el diccionario si existe."""
    for p in inventario:
        if p['nombre'].lower() == nombre.lower():
            return p
    return None


# AGREGAR PRODUCTO
def agregar_producto(inventario):
    """Agrega un producto nuevo o suma cantidad si ya existe."""
    print('Agregando producto:\n')
    
    nombre = input('Ingrese el nombre del producto: ').strip().title()
    precio = float(input('Ingrese el precio del producto: '))
    cantidad = int(input('Ingrese la cantidad del producto: '))
    
    p = buscar_producto(nombre, inventario)
    
    if p:
        print(f'El producto "{nombre}" ya existe en el inventario.')
            
        sumar = input('¿Desea sumar la cantidad ingresada al producto existente? (si/no): ').lower()
            
        if sumar in ('si', 'sí', 's'):
            p['cantidad'] += cantidad
            print('La cantidad se sumó correctamente.\n')
        
        elif sumar in ('no', 'n'):
            print('No se sumó la cantidad y no se agregó un producto nuevo.\n')
        
        else:
            print('Opción no reconocida.\n')
            
    else:
        producto = {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
        inventario.append(producto)
        print('Producto agregado exitosamente.\n')


# MOSTRAR INVENTARIO
def mostrar_inventario(inventario):
    """Muestra los productos del inventario."""
    print('Mostrando inventario:\n')
    
    if len(inventario) == 0:
        print('No hay productos registrados.\n')
        return
    
    for p in inventario:
        print(f"{p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']}")
    print()


# MODIFICAR PRODUCTO
def modificar_producto(inventario):
    """Permite modificar nombre, precio o cantidad de un producto."""
    print('Modificando producto:\n')
    
    producto = input('¿Qué producto desea modificar?: ').strip().title()
    p = buscar_producto(producto, inventario)

    if p:
        print(f"\nNombre: {p['nombre']}\nPrecio: ${p['precio']}\nCantidad: {p['cantidad']}\n")
        
        while True:
            print('Datos disponibles para modificar:')
            print('1. Nombre')
            print('2. Precio')
            print('3. Cantidad')
            print('4. Salir')
            
            cambio = int(input('¿Qué dato desea modificar?: '))
            
            if cambio == 1:
                nuevo_nombre = input(f'Nuevo nombre para "{p["nombre"]}": ')
                p['nombre'] = nuevo_nombre.strip().title()
            
            elif cambio == 2:
                nuevo_precio = float(input(f'Nuevo precio (actual ${p["precio"]}): '))
                p['precio'] = nuevo_precio
            
            elif cambio == 3:
                nueva_cantidad = int(input(f'Nueva cantidad (actual {p["cantidad"]}): '))
                p['cantidad'] = nueva_cantidad
            
            elif cambio == 4:
                break
            
            else:
                print('Opción no válida.\n')
                
    else:
        print(f'El producto "{producto.lower()}" no existe en el inventario.\n')


# ELIMINAR PRODUCTO
def eliminar_producto(inventario):
    """Elimina un producto del inventario si existe."""
    print('Eliminando producto:\n')
    
    producto = input('¿Qué producto desea eliminar?: ').strip().title()
    p = buscar_producto(producto, inventario)
    
    if p:
        print(f"\nNombre: {p['nombre']}\nPrecio: ${p['precio']}\nCantidad: {p['cantidad']}\n")
        
        eliminado = input('¿Desea eliminar este producto? (si/no): ').lower()
        
        if eliminado in ('si', 'sí', 's'):
            inventario.remove(p)
            print('El producto se eliminó correctamente.\n')
        
        elif eliminado in ('no', 'n'):
            print('El producto no será eliminado.\n')
            
        else:
            print('Opción no válida.\n')


# BUCLE PRINCIPAL
while True:
    mostrar_menu()
    eleccion = int(input('Ingrese el número de la opción deseada: '))
    print()

    if eleccion == 1:
        agregar_producto(inventario)

    elif eleccion == 2:
        mostrar_inventario(inventario)

    elif eleccion == 3:
        modificar_producto(inventario)

    elif eleccion == 4:
        eliminar_producto(inventario)

    # SALIR DEL PROGRAMA
    elif eleccion == 5:
        print('\nHasta luego.\n')
        break

    else:
        print('\nOpción inválida. Intente nuevamente.\n')