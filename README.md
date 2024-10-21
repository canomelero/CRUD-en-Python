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
