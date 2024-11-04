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
    fecha_pedido DATE
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