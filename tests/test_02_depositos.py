import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.feria import Feria
from src.tarjeta import Tarjeta
from src.db_connection import get_conn


def test_deposito():
    print("=== DEPOSITO ===")
    feria = Feria()

    t = Tarjeta.crear("DepositoTest")
    saldo_inicial = t.saldo
    monto = 150.0

    t_actualizada = feria.depositar(t.id, monto)
    print(f"Tarjeta después del depósito -> id={t_actualizada.id}, saldo={t_actualizada.saldo}")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT saldo FROM tarjetas WHERE id=%s",
        (t.id,)
    )
    saldo_db = float(cur.fetchone()[0])

    cur.execute(
        """SELECT tipo, monto, descripcion
           FROM transacciones
           WHERE tarjeta_id = %s AND tipo='DEPOSITO'
           ORDER BY id DESC LIMIT 1""",
        (t.id,)
    )
    trans = cur.fetchone()
    print("Última transacción de depósito:", trans)

    cur.execute("DELETE FROM transacciones WHERE tarjeta_id=%s", (t.id,))
    cur.execute("DELETE FROM tarjetas WHERE id=%s", (t.id,))
    conn.commit()

    cur.close()
    conn.close()

    assert saldo_db == saldo_inicial + monto
    assert trans is not None
    assert trans[0] == "DEPOSITO"
    assert float(trans[1]) == monto
