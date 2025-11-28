# tarjeta.py
from db_connection import get_conn

class Tarjeta:
    def __init__(self, id_, nombre, saldo=0.0):
        self.id = id_
        self.nombre = nombre
        self.saldo = float(saldo)

    @classmethod
    def crear(cls, nombre):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tarjetas (nombre, saldo) VALUES (%s, %s)",
                (nombre, 0.0)
            )
            conn.commit()
            tid = cur.lastrowid
            return cls(tid, nombre, 0.0)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, saldo FROM tarjetas ORDER BY id")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2]) for r in rows]
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, saldo FROM tarjetas WHERE id = %s", (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2]) if r else None
        finally:
            cur.close()
            conn.close()

    def guardar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE tarjetas SET nombre=%s, saldo=%s WHERE id=%s",
                (self.nombre, self.saldo, self.id)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()

    @classmethod
    def eliminar(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM tarjetas WHERE id=%s", (id_,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
