# CRUD en Python
Proyecto realizado con Python que consiste en realizar un CRUD (Create, Read, Update, Delete).

El Sistema Gestor de Base de Datos (SGDB) utilizado es PostgreSQL y la base de datos creada contará con tres tablas: 

  - Stock: se almacenarán los datos relacionados con los artículos disponibles, tanto su producto como la cantidad de cada uno.
  - Pedido: se almacenarán los datos relacionados con un pedido, siendo éstos el código del pedido, el código del cliente que realiza el pedido y la fecha del pedido.
  - Detalle-pedido: se almacenará la información de un pedido sobre un artículo que está en stock.

## Tecnologías utilizadas
  - Python
  - PostgreSQL
  - Psyco2pg (driver para la conexión a la base de datos)
  - Anaconda (entorno virtual)

## Instalación de PostgreSQL en Anaconda
Paso 1. Instalación de Anaconda.

Paso 2. Creación de un entorno virtual de Anaconda. Una vez instalado, se abre un terminal y se ejecutan los siguientes comandos:
  ```
  conda create -n CRUD python # Crear entorno virtual
  conda activate CRUD # Activar entorno virtual
  conda install -c anaconda postgresql # Instalar PostgreSQL
  conda install -c anaconda psycopg2 # Instalar driver de Python para PostgreSQL
  ```
Paso 3. Inicialización de PostgreSQL y creación de una base de datos. Para ello, se abre un terminal y se ejecutan los siguientes comandos:
  ```
  conda activate DDSI # Activar entorno virtual
  initdb ./pgdata # Crear database cluster directory
  pg_ctl -D ./pgdata -l logfile start # Iniciar PostgreSQL
  ```
El comando pg_ctl crea un directorio llamado pgdata en el directorio actual. Este directorio contiene los archivos de configuración de PostgreSQL. Se puede sustituir ./pgdata por cualquier otro directorio. El comando pg_ctl también inicia el servidor de PostgreSQL. Para detener el servidor, se ejecuta el siguiente comando:
  ```
  pg_ctl -D ./pgdata stop # Detener PostgreSQL
  ```
En este punto, ya se puede iniciar sesión en PostgreSQL para conectarse a una base de datos:
  ```
  psql -l # Listar bases de datos
  psql -d postgres # Conectarse a la base de datos postgres
  ```
Si lo desea, una vez dentro de PostgreSQL, se puede crear un nuevo usuario y darle permisos de SUPERUSUARIO:
  ```
  CREATE USER usuario WITH PASSWORD 'password'; # Crear usuario
  ALTER USER usuario WITH SUPERUSER; # Dar permisos de superusuario al usuario
  \q # Salir de PostgreSQL
  ```

