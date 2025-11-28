# tienda.py
from db_connection import get_conn

class Tienda:
    def __init__(self, id_, nombre):
        self.id = id_
        self.nombre = nombre

    @classmethod
    def crear(cls, nombre):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO tiendas (nombre) VALUES (%s)", (nombre,))
            conn.commit()
            tid = cur.lastrowid
            return cls(tid, nombre)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM tiendas ORDER BY id")
            rows = cur.fetchall()
            return [cls(r[0], r[1]) for r in rows]
        finally:
            cur.close()
            conn.close()
