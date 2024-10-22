# Librería que permite leer y escribir sobre ficheros
import os

# Adaptador para PostgreSQL en Python
import psycopg2 as pg  



# Variables globales para mostrar el menú por pantalla
menu = """
    \n.: Menú :.
        1. Borrado y creación de tablas con inserción de 10 tuplas 
        2. Dar de alta nuevo pedido
        3. Mostrar contenido de las tablas de la BD
        4. Salir del programa y cerrar conexión a la BD
        ¿Qué acción desea realizar?: 
    """
menu2 = """
    Opciones:
        1. Añadir detalle de producto
        2. Eliminar todos los detalles del producto
        3. Cancelar el pedido
        4. Finalizar pedido 
    """

def ejecucion(connection, cursor) -> None:
    """Ejecuta las distintas funcionalidades del código.

    Parameters
    ----------
    connection : psycopg2.connection
        Objeto con la conexión realizada a la base de datos.
    cursor : psycopg2.cursor
        Cursor a la base de datos de la conexión realizada.
    
    Return
    ------
    None
    """

    opcion = int(input(menu))
    opcion2 = str()

    # Variables para recoger los datos del pedido y stock
    cpedido = str()
    ccliente = str()
    fecha_pedido = str()
    cproducto = str()
    cantidad_stock = str()
    savepoint_1 = "SAVEPOINT S1;"
    
    # Contenido
    while opcion != 4:
        if opcion == 1:
           cursor.execute(savepoint_1)
           crear_tablas(cursor)
            
        elif opcion == 2:
            cursor.execute(savepoint_1) # CREAR UN NUEVO SAVEPOINT ?????

            # Asignar cada valor de la tupla devuelva a cada variable
            cpedido, ccliente, fecha_pedido = aniadir_pedido(cpedido, ccliente, 
                                                            fecha_pedido)
            # Opciones a realizar con el pedido
            opcion2 = int(input(menu2))

            while opcion2 == 1 or opcion2 == 2:
                # PONER AQUÍ UN SAVEPOINT ?????
                if opcion2 == 1:
                    cproducto, cantidad_pedida, cantidad_stock = obtener_cantidad_producto(
                                                            cproducto, cantidad_stock)
                    aniadir_detalles_pedido(cpedido, cproducto, cantidad_pedida) 
                
                elif opcion2 == 2:
                    eliminar_detalles_pedido(cpedido)   # NECESARIO HACER UN COMMIT ?????
            
                opcion2 = int(input(menu2))

            if opcion2 == 3:
                eliminar_detalles_y_pedido(cpedido)    # NECESARIO HACER UN COMMIT ???? 

            elif opcion2 == 4:
                print("Guardando los cambios realizados y saliendo...")
                connection.commit();   
        
        elif opcion == 3:
            mostrar_tablas()
            
        opcion = int(input(menu));


def crear_tablas(cursor) -> None:
    """Crea las tablas en una base de datos a partir de un archivo.

    Parameters
    ----------
    cursor : psycopg2.cursor
        Cursor a la base de datos de la conexión realizada.

    Returns
    -------
    None
    """

    print("Creación de tablas e inserción de tuplas en Stock...")

    # getcwd() -> Devuelve un string que representa el directorio de trabajo actual
    print("Indique el nombre archivo .sql desde la ruta actual (ponga /nombre_archivo.sql):")
    path = os.getcwd() + input()

    try:  
        # Abrir el archivo proporcionado en formato sql, el cual contiene las tablas a crear
        # junto a algunos datos.
        with open(path, "r") as archivo:
            cursor.execute(archivo.read())
    except Exception as e:
        print("Error en la lectura del archivo")
        cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise e

    connection.commit()


def aniadir_pedido(cpedido: str, ccliente: str, fecha_pedido: str) -> tuple:
    """Añade una nueva tupla a la tabla pedido

    Parameters
    ----------
    cpedido : str
        Código del pedido a insertar. Es la calve primaria de la tabla pedido.
    ccliente : str
        Código del cliente que realiza el pedido.
    fecha_pedido : str
        Fecha en la que se ha realizado el pedido.

    Returns
    -------
    tuple
        Valores que ha proporcionado el cliente para añadir el pedido.
    """

    cpedido = input("Código del pedido: ")
    ccliente = int(input("Código del cliente: "))
    fecha_pedido = input("Fecha del pedido: ")  # De tipo DATE o VARCHAR

    try:
        # Introducir los datos en la tabla pedido.
        cursor.execute(
            "INSERT INTO pedido(cpedido, ccliente, fecha_pedido) VALUES (%s, %s, %s);",
            (cpedido, ccliente, fecha_pedido)
        )
    except Exception as e:
        print("No se ha podido insertar el pedido")
        cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise e

    return (cpedido, ccliente, fecha_pedido)
    

def obtener_cantidad_producto(cproducto: str, cantidad_stock: int) -> tuple:
    """Obtiene la cantidad de producto que desea el cliente.

    Esta función obtiene la cantidad del producto porporcionado por su código de producto,
    que desea el cliente. Además comprueba que no ha solicitado más productos del que 
    hay disponible en la tabla stock.

    Parameters
    ----------
    cproducto : str
        Código del producto a obtener.
    cantidad_stock : int
        Existencias restantes del producto solicitado (sin reducir por la cantida 
        solicitada de dicho producto).

    Returns
    -------
    tuple
        Código del producto solicitado, la cantidad de dicho producto obtenida y la 
        cantidad de stock que hay de dicho producto.

    Raises
    ------
    Exception
        En caso de que haya 0 existencias del producto solicitado.
    Exception
        Si se solicita más productos de los que hay en la tabla stock.
    """

    print("Detalles del producto...")
    cproducto = input("Código del producto: ")
    cantidad_pedida = int(input("Cantidad de artículos: "))

    try:
        cursor.execute("SELECT cantidad FROM stock WHERE cproducto = %s;", (cproducto,))
        cantidad_stock = cursor.fetchone()[0]

        if not cantidad_stock:
            raise Exception("No hay artículos disponibles")
        elif int(cantidad_stock) < cantidad_pedida:
            raise Exception("No hay suficiente cantidad de artículos")
    except Exception as e:
        print("No se ha podido obtener la cantidad del artículo") 
        cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise e  
        
    return (cproducto, cantidad_pedida, cantidad_stock)


def aniadir_detalles_pedido(cpedido: str, cproducto: str, cantidad_pedida: int) -> None:
    """Añade los valores obtenidos por la función obtener_cantidad_producto() y actualiza
       las existencias restantes de dicho producto.

    Parameters
    ----------
    cpedido : str
        Código del pedido realizado.
    cproducto : str
        Código del producto que se ha solicitado.
    cantidad_pedida : int
        Cantidad solicitada del código de producto en específico.

    Returns
    -------
    None
    """

    print("Añadiendo los detalles del pedido...")

    try:
        cursor.execute(
            "INSERT INTO detalle_pedido(cpedido, cproducto, cantidad) VALUES (%s, %s, %s);",
            (cpedido, cproducto, cantidad_pedida)
        )
        cursor.execute(
            "UPDATE stock SET cantidad = cantidad - %s WHERE cproducto = %s;",
            (cantidad_pedida, cproducto)
        )
    except Exception as e:
        print("No ha sido posible añadir los detalles del producto")
        cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise e


def eliminar_detalles_pedido(cpedido: str) -> None:
    """Elimina una tupla de la tabla detalle_pedido.

    Parameters
    ----------
    cpedido : str
        Código del pedido de la tupla a eliminar.
    
    Returns
    -------
    None
    """

    print("Eliminando detalles del pedido...")

    try:
        cursor.execute("DELETE FROM detalle_pedido WHERE cpedido = %s;", (cpedido,))
    except Exception as e:
        print("No ha sido posible eliminar los detalles del pedido")
        cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise e


def eliminar_detalles_y_pedido(cpedido: str) -> None:
    """Elimina la tupla de la tabla detalles_pedido y de la tabla pedidos.

    Para eliminar la tupla de la tabla detalles_pedido se llama a la función eliminar_
    detalles_pedido(). Después de llamar a dicha función, elimina el pedido de la tabla
    pedido.

    Parameters
    ----------
    cpedido : str
        Código del pedido de la tupla a eliminar.

    Returns
    -------
    None
    """

    print("Eliminando pedido...")
    
    try:
        eliminar_detalles_pedido(cpedido)
        cursor.execute("DELETE FROM pedido WHERE cpedido = %s;", (cpedido,))
    except Exception as e:
        print("No ha sido posible eliminar el pedido")
        cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise e
    

def mostrar_tablas() -> None:
    """Muestra el contenido actual de las tablas que se encuentran en la base de datos
       en la que estás conectado.

    Returns
    -------
    None
    """

    print("Listando la Base de Datos...")
    print("Tabla Pedido:")

    cursor.execute("SELECT * FROM pedido;")
    tablaPedido = cursor.fetchall()

    for pedido in tablaPedido:
        print(pedido)

    print("\nTabla Stock:")

    cursor.execute("SELECT * FROM stock;")
    tablaStock = cursor.fetchall()

    for artSotck in tablaStock:
        print(artSotck)

    print("\nTabla Detalle-Pedido:")

    cursor.execute("SELECT * FROM detalle_pedido;")
    tablaDetallePed = cursor.fetchall()

    for detallePedido in tablaDetallePed:
        print(detallePedido)


if __name__=='__main__':
    # Conexión a la base de datos
    connection = pg.connect(
        database = 'pedidos',
        user = 'ddsiuser',
        password = 'ddsi',
        host = 'localhost'
    )

    # Se desactiva el commit automático para que no lo realice cada
    # vez que se realiza un INSERT, UPDATE, etc
    connection.autocommit = False

    try:
        cursor = connection.cursor();
        ejecucion(connection, cursor)
    except Exception as e:
        print(e)

    # Aunque se ejecute correctamente el try o el except, siempre va a ejecutar 
    # el código que hay en el finally.
    finally:
        cursor.close()
        connection.close()
        print("Programa finalizado")
