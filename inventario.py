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
        print('Agregando producto: \n')
        
        nombre = input('Ingrese el nombre del producto: ')
        precio = float(input('Ingrese el precio del producto: '))
        cantidad = int(input('Ingrese la cantidad del producto: '))

        producto = {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}
        inventario.append(producto)

        print('\nProducto añadido exitosamente.\n')
        print()

    elif eleccion == 2:
        print('\nOpción no declarada.\n')
        print()

    elif eleccion == 3:
        print('\nOpción no declarada.\n')
        print()

    elif eleccion == 4:
        print('\nOpción no declarada.\n')
        print()

    elif eleccion == 5:
        print('\nHasta luego.\n')
        break

    else:
        print('\nOpción inválida. Intente nuevamente.\n')