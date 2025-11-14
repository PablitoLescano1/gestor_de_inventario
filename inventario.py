# Sistema de Inventario
# Autor: Stéfano Bertone

print('\nGESTOR DE INVENTARIO\n')

def mostrar_menu():
    print('Menú principal\n')
    print('1. Agregar producto')
    print('2. Mostrar producto')
    print('3. Modificar producto')
    print('4. Eliminar producto')
    print('5. Salir\n')


inventario = []

while True:
    mostrar_menu()
    eleccion = int(input('Ingrese el número de la opción deseada: '))
    print()

    # agregar producto
    if eleccion == 1:
        print('Agregando producto:\n')
        
        nombre = input('Ingrese el nombre del producto: ').strip().title()
        precio = float(input('Ingrese el precio del producto: '))
        cantidad = int(input('Ingrese la cantidad del producto: '))
        
        for i in inventario:
            if nombre.lower() == i['nombre'].lower():
                print(f'El producto "{nombre}" ya existe en el inventario')
                
                sumar = input('¿Desea sumar la cantidad ingresada al producto ya existente? (si/no): ')
                
                if sumar.lower() in ('si', 'sí'):
                    i['cantidad'] += cantidad
                    print('La cantidad se sumó efectivamente.\n')
                else:
                    print('No se sumó la cantidad y no se agregó un producto nuevo.\n')
                break
        else:
            producto = {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
            inventario.append(producto)
            print('Producto añadido exitosamente.\n')

    # mostrar producto
    elif eleccion == 2:
        if len(inventario) == 0:
            print('No hay productos registrados.\n')
            continue

        for p in inventario:
            print(f"{p['nombre']} | Precio: ${p['precio']} | Cantidad: {p['cantidad']}")
        print()

    elif eleccion == 3:
        print('\nOpción no declarada.\n')

    elif eleccion == 4:
        print('\nOpción no declarada.\n')

    elif eleccion == 5:
        print('\nHasta luego.\n')
        break

    else:
        print('\nOpción inválida. Intente nuevamente.\n')
