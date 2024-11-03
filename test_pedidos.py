# Para poder hacer uso de esta librería poner: conda install -c anaconda pytest
# En caso de querer probar en vuestro ubuntu poner: sudo apt install pytest
# Para ejecutar los test en el entorno virtual de DDSI poner: pytest test_pedidos.py
# Si queréis ver el por qué algunos test aparecen con 's' (están desactivados). Poner:
# pytest -rs test_pedidos.py
# Cualquier otra duda os miráis la documentación nenes <3.
import pytest  
import psycopg2

from psycopg2 import errors
from pedidos_clase import Pedidos

@pytest.fixture
def conexion_bd():
    conexion = Pedidos()
    yield conexion
    conexion.cerrar_conex()

@pytest.mark.skip(reason="Desactivado para no crear las tablas todo el rato")
def test_crear_tablas_y_comprobar_valores(conexion_bd):
    conexion_bd.crear_tablas("/pedidos.sql")
    valores_stock = conexion_bd.obtener_stock()
    valores_esperados = [
        ('1a', 4),
        ('2a', 2),
        ('3a', 5),
        ('4a', 1),
        ('5a', 2),
        ('6a', 8),
        ('7a', 6),
        ('8a', 9),
        ('9a', 3),
        ('10a', 4),
    ]
    assert valores_stock == valores_esperados


def test_crear_tablas_archivo_incorrecto(conexion_bd):
    with pytest.raises(Exception):
        conexion_bd.crear_tablas("pedid.sql")


@pytest.mark.skip(reason="Test desactivado temporalmente para evitar respuestas incorrectas")
def test_aniadir_pedido_correcto(conexion_bd):
    conexion_bd.aniadir_pedido("1234", 345, "16-07-2023")
    valores_anidadidos = conexion_bd.obtener_pedido()
    conexion_bd.connection.commit()

    assert valores_anidadidos == [("1234", 345, "16-07-2023")]


# Generar lista de valores incorrectos con las repsectivas excepciones que lanza
# cada tupla.
@pytest.mark.parametrize("valores_inco_pedidos, excep_esp", [
    (("1234", 346, "16-07-2023"), errors.UniqueViolation),
    (("123456789", 345, "18-07-2023"), errors.StringDataRightTruncation),
    (("12", 345, "2023-18-07"), errors.DatetimeFieldOverflow),
    (("13", "abcdef", "2023-18-07"), errors.InvalidTextRepresentation)
])

# Este test va recorriendo en un bucle toda la lista creada anteriormente y comprueba
# que todos los valores proporcionados en dicha lista, lanza la excepción adecuada.
def test_aniadir_cod_pedido_incorrecto(conexion_bd, valores_inco_pedidos, excep_esp):
    with pytest.raises(excep_esp):
        # El * se usa para separa los valores de la tupla en valores individuales
        conexion_bd.aniadir_pedido(*valores_inco_pedidos)
        conexion_bd.connection.commit()


def test_obtener_cantidad_producto(conexion_bd):
    conexion_bd.obtener_cantidad_producto("1a", "4")
    conexion_bd.connection.commit()

    assert (conexion_bd.cproducto, conexion_bd.cantidad_pedida) == ("1a", "4")

def test_obtener_cantidad_producto_cp_no_existe(conexion_bd):
    with pytest.raises(errors.UndefinedColumn):
        conexion_bd.obtener_cantidad_producto("12a", "4")
        conexion_bd.connection.commit()


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#
# No se han hecho test de la función aniadir_detalle_pedido() ya que todos los 
# valores que se usan se comprueba con los anteriores test en las anteriores 
# funciones por lo que es rebundante comprobar lo mismo de nuevo.
#
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
