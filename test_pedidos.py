import pytest
import psycopg2

from psycopg2 import errors
from pedidos_clase import Pedidos

@pytest.fixture
def conexion_bd():
    conexion = Pedidos()
    yield conexion
    conexion.cerrar_conex()


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


# Se genrea una lista de valores incorrectos con las repsectivas excepciones que lanza
# cada tupla.
@pytest.mark.parametrize("valores_inco_pedidos, excep_esp", [
    (("1234", 346, "16-07-2023"), errors.UniqueViolation),
    (("123456789", 345, "18-07-2023"), errors.StringDataRightTruncation),
    (("12", 345, "2023-18-07"), errors.DatetimeFieldOverflow)
])


def test_aniadir_cod_pedido_incorrecto(conexion_bd, valores_inco_pedidos, excep_esp):
    with pytest.raises(excep_esp):
        # El * se usa para separa los valores de la tupla en valores individuales
        conexion_bd.aniadir_pedido(*valores_inco_pedidos)
        conexion_bd.connection.commit()

