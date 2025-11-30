from inventario import (
    inventario,
    campos,
    agregar_producto,
    mostrar_inventario,
    modificar_producto,
    eliminar_producto,
    validar_dato,
    ordenar_y_mostrar,
    crear_campo,
)

print('\nGESTOR DE INVENTARIO\n')


def mostrar_menu():
    """Menú principal del sistema."""
    print('Menú principal:\n')
    print('1. Crear campo.')
    print('2. Agregar producto.')
    print('3. Mostrar inventario.')
    print('4. Modificar producto.')
    print('5. Eliminar producto.')
    print('6. Salir.\n')


while True:
    mostrar_menu()
    eleccion = validar_dato('Ingrese el número de la opción deseada: ', int)
    print()

    if eleccion == 1:
        nombre = input("Ingrese el nombre del campo que desea agregar: ").strip()
        tipo = input('Tipo de dato ("texto", "num entero", "num decimal", "v/f", "fecha"): ').strip()

        ok, err = crear_campo(campos, nombre, tipo)

        if ok:
            print("Campo creado correctamente.\n")
        else:
            print("Error:", err, "\n")

    elif eleccion == 2:
        agregar_producto(inventario, campos)

    elif eleccion == 3:
        ordenar_y_mostrar(inventario)

    elif eleccion == 4:
        modificar_producto(inventario)

    elif eleccion == 5:
        eliminar_producto(inventario)

    elif eleccion == 6:
        print('\nHasta luego.\n')
        break

    else:
        print('\nOpción no válida. Intente nuevamente.\n')