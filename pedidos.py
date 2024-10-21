# Adaptador para PostgreSQL en Python
import psycopg2 as pg   

# Conexión a la base de datos (ODBC)
connection = pg.connect(
    database = 'pedidos',
    user = 'ddsiuser',
    password = 'ddsi',
    host = 'localhost'
)

# Se desactiva el commit automático para que no lo realice cada
# vez que se realiza un INSERT, UPDATE, etc
connection.autocommit = False

# Variables
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
opcion = int(input(menu))
opcion2 = ''

# Variables para recoger los datos del pedido y stock
cpedido = ''
ccliente = ''
fecha_pedido = ''
cproducto = ''
cantStock = ''

# Creación de un cursor 
# Éste permite la ejecución de comandos de PostgreSQL en una base de datos
cursor = connection.cursor();
cursor.execute("BEGIN;")
cursor.execute("SAVEPOINT s1;")

# Contenido
while opcion != 4:
    if(opcion == 1):
        print("Creación de tablas e inserción de tuplas en Stock...")
        
        try:
            crearPedidosScript = """
                DROP TABLE IF EXISTS stock CASCADE;
                DROP TABLE IF EXISTS pedido CASCADE;
                DROP TABLE IF EXISTS detalle_pedido CASCADE;

                CREATE TABLE IF NOT EXISTS stock (
                    cproducto VARCHAR(5) PRIMARY KEY,
                    cantidad INT
                );

                CREATE TABLE IF NOT EXISTS pedido (
                    cpedido VARCHAR(5) PRIMARY KEY,
                    ccliente INT,
                    fecha_pedido VARCHAR(10) 
                );

                CREATE TABLE IF NOT EXISTS detalle_pedido (
                    cpedido VARCHAR(5),
                    cproducto VARCHAR(5),
                    cantidad INT,
                    FOREIGN KEY(cpedido) REFERENCES pedido(cpedido),
                    FOREIGN KEY(cproducto) REFERENCES stock(cproducto),
                    PRIMARY KEY(cpedido, cproducto)
                );

                INSERT INTO stock VALUES ('1a', 4);
                INSERT INTO stock VALUES ('2a', 2);
                INSERT INTO stock VALUES ('3a', 5);
                INSERT INTO stock VALUES ('4a', 1);
                INSERT INTO stock VALUES ('5a', 2);
                INSERT INTO stock VALUES ('6a', 8);
                INSERT INTO stock VALUES ('7a', 6);
                INSERT INTO stock VALUES ('8a', 9);
                INSERT INTO stock VALUES ('9a', 3);
                INSERT INTO stock VALUES ('10a', 4);
            """

            cursor.execute(crearPedidosScript)
            connection.commit()
        except Exception as e:
            cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            cursor.execute("RELEASE SAVEPOINT s1;")
            raise e
        
    elif(opcion == 2):
        # Capturar datos del pedido
        cpedido = input("Código del pedido: ")
        ccliente = int(input("Código del cliente: "))
        fecha_pedido = input("Fecha del pedido: ")  # De tipo DATE o VARCHAR

        # Se introducen los datos en la tabla pedido
        try:
            cursor.execute(
                "INSERT INTO pedido(cpedido, ccliente, fecha_pedido) VALUES (%s, %s, %s);",
                (cpedido, ccliente, fecha_pedido)
            )
        except Exception as e:
            cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            cursor.execute("RELEASE SAVEPOINT s1;")
            raise e
        
        # Opciones a realizar con el pedido
        opcion2 = int(input(menu2))

        while opcion2 == 1 or opcion2 == 2:
            if(opcion2 == 1):
                print("Detalles del producto...")
                cproducto = input("Código del producto: ")
                cantPedida = int(input("Cantidad de artículos: "))

                try:
                    cursor.execute("SELECT cantidad FROM stock WHERE cproducto = %s;", (cproducto,))

                    # fectone() -> devuelve una tupla (si la hay) en la BD
                    cantStock = cursor.fetchone()[0]
                    
                    if cantStock < cantPedida:
                        raise Exception("No hay suficiente cantidad de artículos")
                except Exception as e:
                    cursor.execute("ROLLBACK TO SAVEPOINT s1;")
                    cursor.execute("RELEASE SAVEPOINT s1;")
                    raise e
                
                try:
                    cursor.execute(
                        "INSERT INTO detalle_pedido(cpedido, cproducto, cantidad) VALUES (%s, %s, %s);",
                        (cpedido, cproducto, cantPedida)
                    )
                    cursor.execute(
                        "UPDATE stock SET cantidad = cantidad - %s WHERE cproducto = %s;",
                        (cantPedida, cproducto)
                    )
                except Exception as e:
                    cursor.execute("ROLLBACK TO SAVEPOINT s1;")
                    cursor.execute("RELEASE SAVEPOINT s1;")
                    raise e
                
            elif(opcion2 == 2):
                print("Eliminando detalles del producto...")

                try:
                    cursor.execute(
                        "DELETE FROM detalle_pedido WHERE cpedido = %s;",
                        (cpedido)
                    )
                except Exception as e:
                    cursor.execute("ROLLBACK TO SAVEPOINT s1;")
                    cursor.execute("RELEASE SAVEPOINT s1;")
                    raise e 
            
            opcion2 = int(input(menu2))

        if(opcion2 == 3):
            print("Eliminando pedido y sus detalles...")
            
            try:
                cursor.execute("DELETE FROM detalle_pedido WHERE cpedido = %s;", (cpedido))
                cursor.execute("DELETE FROM pedido WHERE cpedido = %s;", (cpedido))    
            except Exception as e:
                cursor.execute("ROLLBACK TO SAVEPOINT s1;")
                cursor.execute("RELEASE SAVEPOINT s1;")
                raise e
             
        elif(opcion2 == 4):
            print("Guardando los cambios realizados...")
            connection.commit();
        
    elif(opcion == 3):
        print("Listando la Base de Datos...")
        print("Tabla Pedido:")

        try:
            cursor.execute("SELECT * FROM pedido;")
            tablaPedido = cursor.fetchall()

            for pedido in tablaPedido:
                print(pedido)
        except Exception as e:
            cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            cursor.execute("RELEASE SAVEPOINT s1;")
            raise e 
        
        print("\nTabla Stock:")

        try:
            cursor.execute("SELECT * FROM stock;")
            tablaStock = cursor.fetchall()

            for artSotck in tablaStock:
                print(artSotck)
        except Exception as e:
            cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            cursor.execute("RELEASE SAVEPOINT s1;")
            raise e 

        print("\nTabla Detalle-Pedido:")

        try:
            cursor.execute("SELECT * FROM stock;")
            tablaDetallePed = cursor.fetchall()

            for detallePedido in tablaDetallePed:
                print(detallePedido)
        except Exception as e:
            cursor.execute("ROLLBACK TO SAVEPOINT s1;")
            cursor.execute("RELEASE SAVEPOINT s1;")
            raise e 

    opcion = int(input(menu));

cursor.close()
connection.close()
print("Programa finalizado")
