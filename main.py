from inventario import (
    inventario,
    agregar_producto,
    mostrar_inventario,
    modificar_producto,
    eliminar_producto,
    validar_dato,
)

print('\nGESTOR DE INVENTARIO\n')

# MENÚ PRINCIPAL
def mostrar_menu():
    """Menú principal del sistema."""
    
    print('Menú principal:\n')
    print('1. Agregar producto.')
    print('2. Mostrar inventario.')
    print('3. Modificar producto.')
    print('4. Eliminar producto.')
    print('5. Salir.\n')

# BUCLE PRINCIPAL
while True:
    mostrar_menu()
    eleccion = validar_dato('Ingrese el número de la opción deseada: ', int)
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