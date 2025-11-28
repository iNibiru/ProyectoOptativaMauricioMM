from db_connection import get_conn

class Transaccion:
    def __init__(self, id_, tarjeta_id, producto_id, tipo, monto, descripcion):
        self.id = id_
        self.tarjeta_id = tarjeta_id
        self.producto_id = producto_id
        self.tipo = tipo
        self.monto = float(monto)
        self.descripcion = descripcion

    @classmethod
    def crear(cls, tarjeta_id, tipo, monto, descripcion="", producto_id=None):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO transacciones
                   (tarjeta_id, producto_id, tipo, monto, descripcion)
                   VALUES (%s, %s, %s, %s, %s)""",
                (tarjeta_id, producto_id, tipo, monto, descripcion)
            )
            conn.commit()
            tid = cur.lastrowid
            return cls(tid, tarjeta_id, producto_id, tipo, monto, descripcion)
        finally:
            cur.close()
            conn.close()
