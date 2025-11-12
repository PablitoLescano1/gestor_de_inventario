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

    if eleccion == 1:
        print('Agregando producto:\n')

        nombre = input('Ingrese el nombre del producto: ')
        precio = float(input('Ingrese el precio del producto: '))
        cantidad = int(input('Ingrese la cantidad del producto: '))

        producto = {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
        inventario.append(producto)

        print('\nProducto añadido exitosamente.\n')

    elif eleccion == 2:
        if len(inventario) == 0:
            print('No hay productos registrados.\n')
            continue

        producto_buscado = input('Ingrese el nombre del producto que desea buscar: ')
        encontrado = False

        for i in inventario:
            if producto_buscado.lower() == i['nombre'].lower():
                print(f"\nNombre: {i['nombre']}\nPrecio: ${i['precio']}\nCantidad: {i['cantidad']}\n")
                encontrado = True
                break

        if not encontrado:
            print('\nEl producto no existe en el inventario.\n')

    elif eleccion == 3:
        print('\nOpción no declarada.\n')

    elif eleccion == 4:
        print('\nOpción no declarada.\n')

    elif eleccion == 5:
        print('\nHasta luego.\n')
        break

    else:
        print('\nOpción inválida. Intente nuevamente.\n')