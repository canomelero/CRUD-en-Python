# Librería que permite leer y escribir sobre ficheros
import os

# Adaptador para PostgreSQL en Python
import psycopg2 as pg  

class Pedidos:
    def __init__(self):
        self.connection = pg.connect(
            database = 'pedidos',
            user = 'ddsiuser',
            password = 'ddsi',
            host = 'localhost'
        )

        self.cursor = self.connection.cursor()
        self.cpedido = str()
        self.ccliente = str()
        self.fecha_pedido = str()
        self.cproducto = str()
        self.cantidad_stock = str()
    
    def crear_tablas(self, archivo : str) -> None:
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
                self.cursor.execute(archivo.read())
        except Exception as e:
            print("Error en la lectura del archivo")
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            raise e


    def aniadir_pedido(self):
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
        """
        self.cursor.execute("SAVEPOINT s1;")

        self.cpedido = input("Código del pedido: ")
        self.ccliente = int(input("Código del cliente: "))
        self.fecha_pedido = input("Fecha del pedido: ")  # De tipo DATE o VARCHAR

        try:
            # Introducir los datos en la tabla pedido.
            self.cursor.execute(
                "INSERT INTO pedido(cpedido, ccliente, fecha_pedido) VALUES (%s, %s, %s);",
                (self.cpedido, self.ccliente, self.fecha_pedido)
            )
        except Exception as e:
            print("No se ha podido insertar el pedido")
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            raise e
        

    def obtener_cantidad_producto(self):
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
        None

        Raises
        ------
        Exception
            En caso de que haya 0 existencias del producto solicitado.
        Exception
            Si se solicita más productos de los que hay en la tabla stock.
        """
        self.cursor.execute("SAVEPOINT s2;")

        print("Detalles del producto...")
        self.cproducto = input("Código del producto: ")
        self.cantidad_pedida = int(input("Cantidad de artículos: "))

        try:
            self.cursor.execute("SELECT cantidad FROM stock WHERE cproducto = %s;", 
                                (self.cproducto,))
            self.cantidad_stock = self.cursor.fetchone()[0]

            if not self.cantidad_stock:
                raise Exception("No hay artículos disponibles")
            elif int(self.cantidad_stock) < self.cantidad_pedida:
                raise Exception("No hay suficiente cantidad de artículos")
            
            self.aniadir_detalles_pedido()
        except Exception as e:
            self.cursor.execute("ROLLBACK TO SAVEPOINT s2;")
            raise e  


    def aniadir_detalles_pedido(self):
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
            self.cursor.execute(
                "INSERT INTO detalle_pedido(cpedido, cproducto, cantidad) VALUES (%s, %s, %s);",
                (self.cpedido, self.cproducto, self.cantidad_pedida)
            )
            self.cursor.execute(
                "UPDATE stock SET cantidad = cantidad - %s WHERE cproducto = %s;",
                (self.cantidad_pedida, self.cproducto)
            )
        except Exception as e:
            print("No ha sido posible añadir los detalles del producto")
            self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            raise e


    def eliminar_detalles_pedido(self) -> None:
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

        self.cursor.execute("ROLLBACK TO SAVEPOINT s2;")

        #try:
        #    self.cursor.execute("DELETE FROM detalle_pedido WHERE cpedido = %s;", (cpedido,))
        #except Exception as e:
        #    print("No ha sido posible eliminar los detalles del pedido")
        #    self.cursor.execute("ROLLBACK TO SAVEPOINT s2;")
        #    raise e


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

        print("Eliminando pedido...")

        self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        
        #try:
        #    eliminar_detalles_pedido(cpedido)
        #    self.cursor.execute("DELETE FROM pedido WHERE cpedido = %s;", (cpedido,))
        #except Exception as e:
        #    print("No ha sido posible eliminar el pedido")
        #    self.cursor.execute("ROLLBACK TO SAVEPOINT s1;")
        #    raise e
        

    def obtener_pedido(cursor) -> list:
        """Obtiene el contenido de la tabla Pedido."""
        cursor.execute("SELECT * FROM pedido;")
        return cursor.fetchall()


    def obtener_stock(cursor) -> list:
        """Obtiene el contenido de la tabla Stock."""
        cursor.execute("SELECT * FROM stock;")
        return cursor.fetchall()


    def obtener_detalle_pedido(cursor) -> list:
        """Obtiene el contenido de la tabla Detalle Pedido."""
        cursor.execute("SELECT * FROM detalle_pedido;")
        return cursor.fetchall()
    
    
    def cerrar_conex(self) -> None:
        self.cursor.close()
        self.connection.close()