from .db_connection import get_conn


class Producto:
    def __init__(self, id_, tienda_id, nombre, precio):
        self.id = id_
        self.tienda_id = tienda_id
        self.nombre = nombre
        self.precio = float(precio)

    @classmethod
    def crear(cls, tienda_id, nombre, precio):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO productos (tienda_id, nombre, precio) VALUES (%s, %s, %s)",
                (tienda_id, nombre, precio)
            )
            conn.commit()
            pid = cur.lastrowid
            return cls(pid, tienda_id, nombre, precio)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_por_tienda(cls, tienda_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, tienda_id, nombre, precio FROM productos WHERE tienda_id=%s",
                (tienda_id,)
            )
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3]) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, tienda_id, nombre, precio FROM productos WHERE id=%s",
                (id_,)
            )
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3]) if r else None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def eliminar(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM productos WHERE id=%s", (id_,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
