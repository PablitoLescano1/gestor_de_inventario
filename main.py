from servicios.campo_servicio import (
    crear_campo,
    modificar_campo,
    eliminar_campo,
    cargar_campos
)

from servicios.inventario_servicio import (
    agregar_producto,
    mostrar_inventario,
    modificar_producto,
    eliminar_producto,
    ordenar_inventario
)

from servicios.busquedas_servicio import buscar_producto


def mostrar_menu():
    print("\nGESTOR DE INVENTARIO")
    print("1. Crear campo")
    print("2. Modificar campo")
    print("3. Eliminar campo")
    print("4. Agregar producto")
    print("5. Mostrar inventario")
    print("6. Modificar producto")
    print("7. Eliminar producto")
    print("8. Salir\n")


def pedir_datos_producto():
    campos = cargar_campos()
    datos = {}

    print("\nComplete los datos del producto:")
    for campo in campos:
        datos[campo] = input(f"{campo}: ").strip()

    return datos


while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        nombre = input("Nombre del nuevo campo: ").strip()
        tipo = input('Tipo ("texto", "num entero", "num decimal", "v/f", "fecha"): ').strip()

        ok, msg = crear_campo(nombre, tipo)
        print(msg if not ok else "Campo creado correctamente.")

    elif opcion == "2":
        nombre = input("Campo a modificar: ").strip()
        nuevo_nombre = input("Nuevo nombre (Enter para no cambiar): ").strip() or None
        nuevo_tipo = input("Nuevo tipo (Enter para no cambiar): ").strip() or None

        ok, msg = modificar_campo(nombre, nuevo_nombre, nuevo_tipo)
        print(msg if not ok else "Campo modificado.")

    elif opcion == "3":
        nombre = input("Campo a eliminar: ").strip()
        ok, msg = eliminar_campo(nombre)
        print(msg if not ok else "Campo eliminado.")

    elif opcion == "4":
        datos = pedir_datos_producto()
        ok, resultado = agregar_producto(datos)

        if ok:
            print("Producto agregado.")
        else:
            print("No se pudo agregar:")
            print(resultado)

    elif opcion == "5":
        ok, lista = mostrar_inventario()
        if not ok:
            print(lista)
        else:
            print("\nINVENTARIO:")
            for fila in lista:
                print(fila)

    elif opcion == "6":
        campo = input("Campo para buscar: ").strip()
        valor = input("Valor a buscar: ").strip()

        nuevos = {}
        print("\nIngrese nuevos valores:")
        while True:
            c = input("Campo (Enter para terminar): ").strip()
            if not c:
                break
            v = input("Nuevo valor: ").strip()
            nuevos[c] = v

        ok, resultado = modificar_producto({campo: valor}, nuevos)

        if ok is True:
            print("Producto modificado.")
        elif ok is None:
            print("Múltiples coincidencias:")
            for p in resultado:
                print(p)
        else:
            print(resultado)

    elif opcion == "7":
        campo = input("Campo para buscar: ").strip()
        valor = input("Valor: ").strip()

        ok, resultado = eliminar_producto({campo: valor})

        if ok is True:
            print("Producto eliminado.")
        elif ok is None:
            print("Múltiples coincidencias:")
            for p in resultado:
                print(p)
        else:
            print(resultado)

    elif opcion == "8":
        print("Hasta luego.")
        break

    else:
        print("Opción inválida.")
