import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest

from src.feria import Feria
from src.tarjeta import Tarjeta
from src.producto import Producto
from src.db_connection import get_conn


def test_compra():
    print("=== COMPRA ===")
    feria = Feria()

    productos_tienda1 = Producto.listar_por_tienda(1)
    if not productos_tienda1:
        pytest.skip("No hay productos en la tienda 1")

    p = productos_tienda1[0]
    print(f"Producto elegido -> id={p.id}, nombre={p.nombre}, precio={p.precio}")

    t = Tarjeta.crear("CompraTest")

    feria.depositar(t.id, p.precio * 2)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT saldo FROM tarjetas WHERE id=%s", (t.id,))
    saldo_antes = float(cur.fetchone()[0])
    print("Saldo antes de compra:", saldo_antes)
    cur.close()
    conn.close()

    t_despues, p_comprado = feria.comprar(t.id, p.id)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT saldo FROM tarjetas WHERE id=%s", (t.id,))
    saldo_db = float(cur.fetchone()[0])
    print("Saldo después de compra (BD):", saldo_db)

    cur.execute(
        """SELECT tipo, monto, descripcion
           FROM transacciones
           WHERE tarjeta_id = %s AND tipo='COMPRA'
           ORDER BY id DESC LIMIT 1""",
        (t.id,)
    )
    trans = cur.fetchone()
    print("Última transacción de compra:", trans)

    cur.execute("DELETE FROM transacciones WHERE tarjeta_id=%s", (t.id,))
    cur.execute("DELETE FROM tarjetas WHERE id=%s", (t.id,))
    conn.commit()

    cur.close()
    conn.close()

    assert saldo_db == saldo_antes - p.precio
    assert trans is not None
    assert trans[0] == "COMPRA"
    assert float(trans[1]) == p.precio
    assert p_comprado.id == p.id
