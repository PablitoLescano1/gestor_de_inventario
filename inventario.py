import json
from datetime import datetime
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

RUTA_CAMPOS = os.path.join(DATA_DIR, "campos.json")
RUTA_INVENTARIO = os.path.join(DATA_DIR, "inventario.json")


def cargar_campos():
    """Carga los campos definidos por el usuario desde campos.json."""
    try:
        with open(RUTA_CAMPOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return {}
            return json.loads(contenido)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def guardar_campos(campos):
    """Guarda los campos definidos por el usuario en campos.json."""
    
    with open(RUTA_CAMPOS, "w", encoding="utf-8") as archivo:
        json.dump(campos, archivo, indent=4, ensure_ascii=False)


campos = cargar_campos()


def cargar_inventario():
    """Carga el archivo inventario.json y devuelve la lista de productos."""
    try:
        with open(RUTA_INVENTARIO, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def guardar_inventario(inventario):
    """Guarda la lista de productos en inventario.json."""
    
    with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


inventario = cargar_inventario()


def producto_duplicado(nuevo, inventario):
    """Devuelve True si existe un producto idéntico (mismo dict) en el inventario."""
    
    for p in inventario:
        if p == nuevo:
            return True
    return False


def buscar_producto(valor_busqueda, inventario, campo_clave):
    """Busca productos cuyo valor en 'campo_clave' coincida parcialmente con 'valor_busqueda'."""
    
    valor_busqueda = str(valor_busqueda).lower().strip()
    
    coincidencias = []

    for producto in inventario:
        valor = str(producto.get(campo_clave, "")).lower()
        
        if valor_busqueda in valor:
            coincidencias.append(producto)

    return coincidencias


def buscar_similares(criterios, inventario):
    """evuelve productos semejantes según varios criterios."""
    
    resultados = []

    for producto in inventario:
        match = True
        for campo, valor in criterios.items():
            valor_producto = str(producto.get(campo, "")).lower()
            valor_busqueda = str(valor).lower()
            
            if valor_busqueda not in valor_producto:
                match = False
                break
            
        if match:
            resultados.append(producto)

    return resultados


def validar_dato(dato, tipo_esperado):
    """Valida y convierte un dato. Devuelve el dato convertido o None si es inválido."""

    if tipo_esperado == str:
        dato = str(dato).strip()
        return dato if dato else None

    if tipo_esperado == bool:
        valor = str(dato).strip().lower()
        if valor in ['si','sí','s','1','true','verdadero','t','y','yes']:
            return True
        if valor in ['no','n','0','false','falso','f']:
            return False
        return None

    if tipo_esperado == int:
        try:
            return int(dato)
        except (ValueError, TypeError):
            return None

    if tipo_esperado == float:
        try:
            return float(dato)
        except (ValueError, TypeError):
            return None

    if tipo_esperado == 'fecha':
        try:
            if isinstance(dato, str):
                datetime.strptime(dato.strip(), '%d-%m-%Y')
                return dato.strip()
            return None
        except (ValueError, AttributeError):
            return None

    return None


def crear_campo(campos, nombre, tipo):
    """Crea un campo nuevo en el diccionario 'campos'."""
    
    if not isinstance(nombre, str) or not nombre.strip():
        return False, "Nombre de campo inválido."
    
    nombre = nombre.strip()
    tipo_normalizado = tipo.strip().lower() if isinstance(tipo, str) else ""
    tipos_validos = ('texto', 'num entero', 'num decimal', 'v/f', 'fecha')

    if tipo_normalizado not in tipos_validos:
        return False, f"Tipo no válido. Debe ser uno de: {', '.join(tipos_validos)}."

    if nombre in campos:
        return False, f'El campo "{nombre}" ya existe.'

    campos[nombre] = tipo_normalizado
    guardar_campos(campos)
    return True, None


def modificar_campo(campos, inventario, nombre_actual, nuevo_nombre=None, nuevo_tipo=None):
    """Modifica un campo existente."""
    
    if nombre_actual not in campos:
        return False, f'El campo "{nombre_actual}" no existe.'

    if not nuevo_nombre and not nuevo_tipo:
        return False, "No se indicó ningún cambio."

    if nuevo_nombre:
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            return False, "El nuevo nombre es inválido."
        
        nuevo_nombre = nuevo_nombre.strip()

        if nuevo_nombre != nombre_actual and nuevo_nombre in campos:
            return False, f'Ya existe un campo llamado "{nuevo_nombre}".'

        tipo_original = campos[nombre_actual]
        del campos[nombre_actual]
        campos[nuevo_nombre] = tipo_original

        for producto in inventario:
            if nombre_actual in producto:
                producto[nuevo_nombre] = producto[nombre_actual]
                del producto[nombre_actual]

    if nuevo_tipo:
        tipo_n = nuevo_tipo.strip().lower()
        tipos_validos = ('texto', 'num entero', 'num decimal', 'v/f', 'fecha')
        if tipo_n not in tipos_validos:
            return False, f"Tipo inválido. Debe ser uno de: {', '.join(tipos_validos)}."

        nombre_final = nuevo_nombre if nuevo_nombre else nombre_actual
        campos[nombre_final] = tipo_n

        for producto in inventario:
            if nombre_final not in producto:
                continue
            valor = producto[nombre_final]
            tipo_py = (
                str if tipo_n == "texto" else
                int if tipo_n == "num entero" else
                float if tipo_n == "num decimal" else
                bool if tipo_n == "v/f" else
                "fecha"
            )
            if validar_dato(str(valor), tipo_py) is None:
                return False, f"El valor '{valor}' no coincide con el tipo '{tipo_n}'."

    guardar_campos(campos)
    guardar_inventario(inventario)
    return True, None


def eliminar_campo(campos, inventario, nombre_campo):
    """Elimina un campo del sistema y de todos los productos."""
    
    if nombre_campo not in campos:
        return False, f'El campo "{nombre_campo}" no existe.'

    if len(campos) == 1:
        return False, "No se puede eliminar el último campo del sistema."

    del campos[nombre_campo]

    for producto in inventario:
        if nombre_campo in producto:
            del producto[nombre_campo]

    guardar_campos(campos)
    guardar_inventario(inventario)
    return True, None


def agregar_producto(inventario, campos, datos, criterios=None, forzar_agregar=False):
    """Agrega un producto validando tipos y devolviendo duplicados si existen."""

    tipo_map = {
        "texto": str,
        "num entero": int,
        "num decimal": float,
        "v/f": bool,
        "fecha": "fecha"
    }

    nuevo_producto = {}
    for campo, tipo_logico in campos.items():
        if campo not in datos:
            return False, f"Falta el campo '{campo}'."

        tipo_py = tipo_map.get(tipo_logico)
        valor_convertido = validar_dato(datos[campo], tipo_py)
        if valor_convertido is None:
            return False, f"Valor inválido para el campo '{campo}'."
        nuevo_producto[campo] = valor_convertido

    duplicados = []
    if criterios and isinstance(criterios, dict):
        duplicados = buscar_similares(criterios, inventario)
    elif producto_duplicado(nuevo_producto, inventario):
        duplicados = [nuevo_producto]

    if duplicados and not forzar_agregar:
        return False, duplicados

    inventario.append(nuevo_producto)
    guardar_inventario(inventario)
    return True, nuevo_producto


def ordenar_inventario(inventario, campo_elegido, modo=1):
    """Ordena el inventario según un campo y modo especificados."""
    
    if not inventario or campo_elegido not in campos:
        return inventario.copy()

    reverse = True if modo == 2 else False
    tipo_campo = campos[campo_elegido]

    def clave(item):
        valor = item.get(campo_elegido)
        if valor is None:
            if tipo_campo in ('num entero', 'num decimal'):
                return float('-inf') if not reverse else float('inf')
            return ""
        if tipo_campo == 'fecha':
            try:
                return datetime.strptime(valor, '%d-%m-%Y')
            except:
                return datetime.min if not reverse else datetime.max
        return valor

    return sorted(inventario, key=clave, reverse=reverse)


def mostrar_inventario(inventario):
    """Devuelve lista de diccionarios."""
    
    resultado = []

    for producto in inventario:
        fila = {}
        for campo in campos:
            valor = producto.get(campo, '-')
            if isinstance(valor, bool):
                valor = 'Sí' if valor else 'No'
            fila[campo] = valor
        resultado.append(fila)

    return resultado


def modificar_producto(inventario, campos, criterios, nuevos_datos):
    """Modifica un producto elegido entre semejantes encontrados."""

    tipo_map = {
        "texto": str,
        "num entero": int,
        "num decimal": float,
        "v/f": bool,
        "fecha": "fecha"
    }

    semejantes = buscar_similares(criterios, inventario)
    if not semejantes:
        return False, "No se encontraron productos semejantes."

    if len(semejantes) > 1:
        return None, semejantes

    producto = semejantes[0]

    for campo, valor_raw in nuevos_datos.items():
        if campo not in campos:
            return False, f"El campo '{campo}' no existe."

        tipo_py = tipo_map.get(campos[campo])
        valor_valido = validar_dato(valor_raw, tipo_py)
        if valor_valido is None:
            return False, f"Valor inválido para el campo '{campo}'."

        producto[campo] = valor_valido

    guardar_inventario(inventario)
    return True, producto


def eliminar_producto(inventario, criterios, producto_elegido=None):
    """Elimina un producto entre los semejantes encontrados."""
    
    semejantes = buscar_similares(criterios, inventario)
    if not semejantes:
        return False, "No se encontraron productos semejantes."

    if producto_elegido is None:
        return None, semejantes

    if producto_elegido in inventario:
        inventario.remove(producto_elegido)
        guardar_inventario(inventario)
        return True, producto_elegido

    return False, "El producto elegido no se encontró en el inventario."