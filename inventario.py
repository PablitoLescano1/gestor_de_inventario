# Sistema de Inventario
# Autor: Stéfano Bertone

print('\nGESTOR DE INVENTARIO\n')

# MENÚ PRINCIPAL
def mostrar_menu():
    print('Menú principal\n')
    print('1. Agregar producto')
    print('2. Mostrar inventario')
    print('3. Modificar producto')
    print('4. Eliminar producto')
    print('5. Salir\n')


# BÚSQUEDA DE PRODUCTO
def buscar_producto(nombre, inventario):
    """Busca un producto por nombre y devuelve el diccionario correspondiente."""
    for p in inventario:
        if p['nombre'].lower() == nombre.lower():
            return p
    return None


inventario = []

# BUCLE PRINCIPAL
while True:
    mostrar_menu()
    eleccion = int(input('Ingrese el número de la opción deseada: '))
    print()

    # AGREGAR PRODUCTO
    if eleccion == 1:
        print('Agregando producto:\n')
        
        nombre = input('Ingrese el nombre del producto: ').strip().title()
        precio = float(input('Ingrese el precio del producto: '))
        cantidad = int(input('Ingrese la cantidad del producto: '))
        
        p = buscar_producto(nombre, inventario)
        
        if p:
            print(f'El producto "{nombre}" ya existe en el inventario.')
                
            sumar = input('¿Desea sumar la cantidad ingresada al producto existente? (si/no): ')
                
            if sumar.lower() in ('si', 'sí', 's'):
                p['cantidad'] += cantidad
                print('La cantidad se sumó correctamente.\n')
            
            elif sumar.lower() in ('no', 'n'):
                print('No se sumó la cantidad y no se agregó un producto nuevo.\n')
            
            else:
                print('Decisión no identificada.\n')
                
        else:
            producto = {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
            inventario.append(producto)
            print('Producto agregado exitosamente.\n')


    # MOSTRAR INVENTARIO
    elif eleccion == 2:
        print('Mostrando inventario:\n')
        
        if len(inventario) == 0:
            print('No hay productos registrados.\n')
            continue
        
        for p in inventario:
            print(f"{p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']}")
        print()


    # MODIFICAR PRODUCTO
    elif eleccion == 3:
        print('Modificando producto:\n')
        
        producto = input('¿Qué producto desea modificar?: ').strip().title()
        
        p = buscar_producto(producto, inventario)

        if p:
            print(f"\nNombre: {p['nombre']}\nPrecio: ${p['precio']}\nCantidad: {p['cantidad']}\n")
            
            while True:
                print('Datos:\n1. Nombre\n2. Precio\n3. Cantidad\n4. Salir')
                cambio = int(input('¿Qué dato desea modificar?: '))
                
                if cambio == 1:
                    nuevo_nombre = input(f'El producto "{p["nombre"]}" será renombrado por: ')
                    p['nombre'] = nuevo_nombre.strip().title()
                
                elif cambio == 2:
                    nuevo_precio = float(input(f'El precio actual es ${p["precio"]}. Ingrese el nuevo precio: '))
                    p['precio'] = nuevo_precio
                
                elif cambio == 3:
                    nueva_cantidad = int(input(f'La cantidad actual es {p["cantidad"]}. Ingrese la nueva cantidad: '))
                    p['cantidad'] = nueva_cantidad
                
                elif cambio == 4:
                    break
                
                else:
                    print('Opción no válida.\n')
                
        else:
            print(f'El producto "{producto.lower()}" no existe en el inventario.\n')


    # ELIMINAR PRODUCTO
    elif eleccion == 4:
        print('Eliminando producto:\n')
        
        producto = input(f'Que prodcuto desea eliminar: ').strip().title()
        
        p = buscar_producto(producto, inventario)
        
        if p:
            print(f"\nNombre: {p['nombre']}\nPrecio: ${p['precio']}\nCantidad: {p['cantidad']}\n")
            
            eliminado = input(f'Desea eliminar dicho producto?(si/no): ').lower()
            if eliminado in ('si', 'sí', 's'):
                inventario.remove(p)
                print('El producto se elimino correctamente')
            
            elif eliminado in ('no', 'n'):
                print('El pruducto no sera eliminado')
                
            else:
                print('Opcion no valida')


    # SALIR
    elif eleccion == 5:
        print('\nHasta luego.\n')
        break


    # OPCIÓN INVÁLIDA
    else:
        print('\nOpción inválida. Intente nuevamente.\n')
