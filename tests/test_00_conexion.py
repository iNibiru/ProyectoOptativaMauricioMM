
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.db_connection import get_conn


def test_database_connection():
    print("=== CONEXION ===")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1")
    row = cur.fetchone()
    print("Resultado SELECT 1:", row)
    cur.close()
    conn.close()
    assert row[0] == 1
