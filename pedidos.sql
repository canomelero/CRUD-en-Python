DROP TABLE IF EXISTS stock CASCADE;
DROP TABLE IF EXISTS pedido CASCADE;
DROP TABLE IF EXISTS detalle_pedido CASCADE;

CREATE TABLE IF NOT EXISTS stock (
    cproducto INT PRIMARY KEY,
    cantidad INT
);

CREATE TABLE IF NOT EXISTS pedido (
    cpedido INT PRIMARY KEY,
    ccliente INT,
    fecha_pedido DATE
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    cpedido INT,
    cproducto INT,
    cantidad INT,
    FOREIGN KEY(cpedido) REFERENCES pedido(cpedido),
    FOREIGN KEY(cproducto) REFERENCES stock(cproducto),
    PRIMARY KEY(cpedido, cproducto)
);

INSERT INTO stock VALUES (1, 4);
INSERT INTO stock VALUES (2, 2);
INSERT INTO stock VALUES (3, 5);
INSERT INTO stock VALUES (4, 1);
INSERT INTO stock VALUES (5, 2);
INSERT INTO stock VALUES (6, 8);
INSERT INTO stock VALUES (7, 6);
INSERT INTO stock VALUES (8, 9);
INSERT INTO stock VALUES (9, 3);
INSERT INTO stock VALUES (10, 4);