# Librería que permite leer y escribir sobre ficheros
import os

# Adaptador para PostgreSQL en Python
import psycopg2 as pg  
from psycopg2 import errors
from tabulate import tabulate

database = str()
user = str()
password = str()

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

def usuario(nombre:str):
    """Inicializar la base de datos en función del usuario que la use"""
    global database, user, password

    if nombre == "GERMÁN":
        database = 'postgres'
        user = 'gag_04'
        password = ''
    
    elif nombre == "JORGE":
        database = 'pedidos'
        user = 'ddsiuser'
        password = 'ddsi'

    elif nombre == "Dani":
        database = "seminario1"
        user = "dani"
        password = "seminario1"
        

class Pedidos:
    """Clase que tiene toda la funcioalidad que es requerida para el seminario 1.

    Esta clase contiene toda la funcionalidad que se requiere en el seminario 1.
    Es decir, maneja todas las tablas adecuadamente junto a los errores que pueden
    ocurrir a lo largo de la consulta e insercción de datos en cada tabla.

    Attributes
    ----------
    cursor : psycopg2.Cursor
        Cursor a la base de datos utilizada.

    cpedido : str
        Código del pedido referenciado de la tabla pedido.

    ccliente : str
        Código del cliente referenciado de la tabla pedido.

    fecha_pedido : str
        Fecha en la que se realiza el pedido (tabla pedido).

    cproducto : str
        Código del producto de la tabla stock.

    cantidad_pedida : str
        Cantidad que se solicita del códio de producto porporcionado.
    """


    def __init__(self):
        #usuario("GERMÁN")
        usuario("JORGE")
        #usuario("Dani")

        global database, user, password

        self.connection = pg.connect(
            dbname=database,  
            user=user,
            password=password,
            host = 'localhost'
        )

        self.cursor = self.connection.cursor()
        self.cpedido = str()
        self.ccliente = str()
        self.fecha_pedido = str()
        self.cproducto = str()
        self.cantidad_pedida = str()
    

    def crear_tablas(self, archivo : str) -> None:
        """Crea las tablas en una base de datos a partir de un archivo.

        Parameters
        ----------
        archivo : str
            Ruta del archivo respecto donde se ejecuta el programa.

        Returns
        -------
        None

        Raises
        ------
        Exception
            Cuando ha ocurrido un error a la hora de leer el archivo, ya sea porque no existe,
            es incorrecta la ruta proporcionada, etc.
        """

        print("Creación de tablas e inserción de tuplas en Stock...")

        path = os.getcwd() + "/" + archivo

        try:  
            # Abrir el archivo proporcionado en formato sql, el cual contiene las tablas a crear
            # junto a algunos datos.
            with open(path, "r") as archivo:
                self.cursor.execute(archivo.read())
        except Exception as e:
            print("Error en la lectura del archivo")
            raise e

        print("Tablas creadas")


    def aniadir_pedido(self, cpedido:str , ccliente: str, fecha_pedido: str):
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
        None

        Raises
        ------
        errors.UniqueViolation
            Se ha proporcionado una clave primaria a una nueva tupla, cuando la clave 
            primaria ya existía anteriormente.

        errors.InvalidDatetimeFormat
            No se ha proporcionado la fecha en formato correcto (DD-MM-YYYY).        

        errors.DateTimeFieldOverflow
            No se ha porporcionado la fecha en el formato europeo (DD-MM-YYYY).

        error.InvlaidTextRepresentation
            Se ha porporcionado un tipo de dato no numérico a la columna código de cliente
            de pedidos.

        Exception
            Cualquier otro error que no tiene que ver con la insercción de valores en la
            tabla pedidos.
        """
        self.cursor.execute("SAVEPOINT s1;")

        try:
            # Introducir los datos en la tabla pedido.
            self.cursor.execute(
                "INSERT INTO pedido(cpedido, ccliente, fecha_pedido) VALUES (%s, %s, %s);",
                (cpedido, ccliente, fecha_pedido)
            )

            print(f"Pedido añadido correctamente: cpedido={cpedido}, ccliente={ccliente}, fecha_pedido={fecha_pedido}")
        except errors.UniqueViolation:
            self.__manejar_excepcion_clave_primaria_pedidos()
        except errors.InvalidDatetimeFormat:
            self.__manejar_excepcion_formato_fecha_pedidos()
        except errors.DatetimeFieldOverflow:
            self.__manejar_excepcion_formato_fecha_incorrecto_pedidos()
        except errors.InvalidTextRepresentation:
            self.__manejar_excepcion_tipo_dato_incorrecto_pedidos()
        except Exception: # Excepción genérica
            print("No se ha podido insertar el pedido")
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            raise
        finally:
            self.cpedido = cpedido
            self.ccliente = ccliente
            self.fecha_pedido = fecha_pedido
        

    def obtener_cantidad_producto(self, cproducto : str, cantidad_pedida : str):
        """Obtiene la cantidad de producto que desea el cliente.

        Esta función obtiene la cantidad del producto porporcionado por su código de producto,
        que desea el cliente. Además comprueba que no ha solicitado más productos del que 
        hay disponible en la tabla stock.

        Parameters
        ----------
        cproducto : str
            Código del producto a obtener de la tabla stock.

        cantidad_pedida : str
            Cantidad de las existencias solicitadas respecto al código de producto (cproducto)
            proporcionado.

        Returns
        -------
        None

        Raises
        ------
        errors.UndefinedColum
            Se ha proporcionado un código de producto que no existe en la tabla stock.

        Exception
            - En caso de que haya 0 existencias del producto solicitado.
            - Si se solicita más productos de los que hay en la tabla stock.
        """

        print("Obteniendo la cantidad del producto...")

        try:
            self.cursor.execute("SELECT cantidad FROM stock WHERE cproducto = %s;", 
                                (cproducto,))
            cantidad_stock = self.cursor.fetchone()

            if not cantidad_stock:
                raise errors.UndefinedColumn
            if not cantidad_stock[0]:
                raise Exception("No hay artículos disponibles")
            elif int(cantidad_stock[0]) < int(cantidad_pedida):
                raise Exception("No hay suficiente cantidad de artículos")
            
            self.cproducto = cproducto
            self.cantidad_pedida = cantidad_pedida

            self.aniadir_detalles_pedido()
        except errors.UndefinedColumn:
            self.__manejar_excepcion_cproducto_no_existe_producto()
        except Exception as e:
            print(e)
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            raise


    def aniadir_detalles_pedido(self):
        """Añade los valores obtenidos por la función obtener_cantidad_producto() y actualiza
        las existencias restantes de dicho producto.

        Returns
        -------
        None
        """

        try:
            self.cursor.execute(
                "INSERT INTO detalle_pedido(cpedido, cproducto, cantidad) VALUES (%s, %s, %s);",
                (self.cpedido, self.cproducto, self.cantidad_pedida)
            )
            self.cursor.execute(
                "UPDATE stock SET cantidad = cantidad - %s WHERE cproducto = %s;",
                (self.cantidad_pedida, self.cproducto)
            )
        except Exception:
            print("No ha sido posible añadir los detalles del producto")
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            raise


    def eliminar_detalles_pedido(self) -> None:
        """Elimina una tupla de la tabla detalle_pedido.
        
        Returns
        -------
        None

        Raises
        ------
        errors.TransactionRollbackError
            No se ha ejecutado correctamente el rollback.
        """

        try:
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        except errors.TransactionRollbackError:
            print("Ha ocurrido un error a la hora de eliminar los detalles del pedido")
            raise


    def eliminar_detalles_y_pedido(self) -> None:
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
        
        try:
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        except errors.TransactionRollbackError():
            print("Ha ocurrido un error a la hora de eliminar los detalles del pedido y el pedido")
            raise
        

    def imprimir_pedido(self) -> None:
        """Obtiene el contenido de la tabla Pedido y lo muestra."""
        self.cursor.execute("SELECT * FROM pedido;")
        valores_pedidos = self.cursor.fetchall()
        
        # Obtener los nombres de columna de la tabla
        columnas = [desc[0] for desc in self.cursor.description]
        
        # Imprimir la tabla en formato ASCII
        print("Contenido de la tabla Pedido:")
        print(tabulate(valores_pedidos, headers=columnas, tablefmt="grid"))


    def imprimir_stock(self) -> None:
        """Obtiene el contenido de la tabla Stock y lo muestra."""
        self.cursor.execute("SELECT * FROM stock;")
        valores_stock = self.cursor.fetchall()
        
        # Obtener los nombres de columna de la tabla
        columnas = [desc[0] for desc in self.cursor.description]
        
        # Imprimir la tabla en formato ASCII
        print("Contenido de la tabla Stock:")
        print(tabulate(valores_stock, headers=columnas, tablefmt="grid"))


    def imprimir_detalle_pedido(self) -> None:
        """Obtiene el contenido de la tabla Detalle Pedido y lo muestra."""
        self.cursor.execute("SELECT * FROM detalle_pedido;")
        valores_detalle_pedidos = self.cursor.fetchall()
        
        # Obtener los nombres de columna de la tabla
        columnas = [desc[0] for desc in self.cursor.description]
        
        # Imprimir la tabla en formato ASCII
        print("Contenido de la tabla Detalle Pedido:")
        print(tabulate(valores_detalle_pedidos, headers=columnas, tablefmt="grid"))
    
    
    def cerrar_conex(self) -> None:
        """Cierra la conexión activa de la base de datos"""
        print("Cerrando conexión...")
        self.cursor.close()
        self.connection.close()
    
    def __manejar_excepcion_clave_primaria_pedidos(self):
        print("""La clave primaria código_pedido ya se encuentra en la base de datos.
                   Recuerda, no se puede duplicar""")
        self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise


    def __manejar_excepcion_formato_fecha_pedidos(self):
        print(f"La fecha proporcionada debería de ser DD-MM-YYYY")
        self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise


    def __manejar_excepcion_formato_fecha_incorrecto_pedidos(self):
        print("El formato de la fecha debe de ser DD-MM-YYYY")
        self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise


    def __manejar_excepcion_tipo_dato_incorrecto_pedidos(self):
        print("En el campo código de cliente se esperaba un valor entero")
        self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise


    def __manejar_excepcion_cproducto_no_existe_producto(self):
        print("El código de producto proporcionado no existe en la tabla stock")
        self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        raise


if __name__ == "__main__":
    # Variables para recoger los datos del pedido y stock
    continuar_ejecucion = True

    cod_pedido = str()
    cod_cliente = str()
    fecha_pedido = str()
    cod_producto = str()
    cantidad_stock = str()

    opcion1 = int(input(menu))
    opcion2 = str()
    pedidos = Pedidos()
    
    while continuar_ejecucion:
        try:
            while opcion1 != 5:
                if opcion1 == 1:
                    archivo_sql = input("Introduzca el nombre del archivo sql: ")
                    pedidos.crear_tablas(archivo_sql)
                        
                elif opcion1 == 2:

                    # Asignar cada valor de la tupla devuelva a cada variable
                    print("..: Datos del pedido :...")
                    cod_pedido = input("Código del pedido: ")
                    cod_cliente = input("Código del cliente: ")
                    fecha_pedido = input("Fecha del pedido: ")
                    pedidos.aniadir_pedido(cod_pedido, cod_cliente, fecha_pedido)
                    
                    # Opciones a realizar con el pedido
                    opcion2 = int(input(menu2))

                    while opcion2 == 1 or opcion2 == 2:                        
                        if opcion2 == 1:
                            print("..: Datos del producto :..")
                            cod_producto = input("Indique el código del producto: ")
                            cantidad_seleccionada = input("Indique la cantidad de producto que desea: ")
                            pedidos.obtener_cantidad_producto(cod_producto, cantidad_seleccionada)
                            # pedidos.aniadir_detalles_pedido() 
                        
                        elif opcion2 == 2:
                            print("Eliminando detalles del pedido...")
                            pedidos.eliminar_detalles_pedido()   
                    
                        opcion2 = int(input(menu2))

                    if opcion2 == 3:
                        print("Eliminando detalles del pedido y pedido...")
                        pedidos.eliminar_detalles_y_pedido() 

                    elif opcion2 == 4:
                        print("Guardando los cambios realizados y saliendo...")
                        pedidos.connection.commit();
                        
                    else:
                        print("Ingrese un valor entre 1-4 (inclusive)")   
                    
                elif opcion1 == 3:
                    pedidos.imprimir_stock()
                    pedidos.imprimir_pedido()
                    pedidos.imprimir_detalle_pedido()
                
                elif opcion1 == 4:
                    continuar_ejecucion = False
                    break
                    
                else:
                    print("Ingrese un valor entre 1-4 (inclusive)")

                opcion1 = int(input(menu)); 
        except Exception as e:
            print("""
                  \n=========================================================================
                  \n=========================================================================
                  \nVolviendo al inicio del programa debido a un error. En caso de querer
                  \nsalir pulse 4 cuando sea posible.
                  \n=========================================================================
                  \n=========================================================================
                """)

    # cerrar conexión cuando finaliza el programa
    pedidos.cerrar_conex()
        