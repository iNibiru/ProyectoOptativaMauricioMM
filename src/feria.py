# feria.py
from tarjeta import Tarjeta
from tienda import Tienda
from producto import Producto
from transaccion import Transaccion

class Feria:
    """Lógica de negocio de la feria."""

    # --- tarjetas ---
    def crear_tarjeta(self, nombre):
        return Tarjeta.crear(nombre)

    def listar_tarjetas(self):
        return Tarjeta.listar_todas()

    def eliminar_tarjeta(self, tarjeta_id):
        Tarjeta.eliminar(tarjeta_id)

    # --- depósitos ---
    def depositar(self, tarjeta_id, monto):
        t = Tarjeta.buscar_por_id(tarjeta_id)
        if not t:
            raise ValueError("Tarjeta no encontrada")
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")

        t.saldo += monto
        t.guardar()

        Transaccion.crear(
            tarjeta_id=t.id,
            tipo="DEPOSITO",
            monto=monto,
            descripcion="Depósito"
        )

        return t

    # --- tiendas ---
    def listar_tiendas(self):
        return Tienda.listar_todas()

    def listar_productos_por_tienda(self, tienda_id):
        return Producto.listar_por_tienda(tienda_id)

    # --- compras ---
    def comprar(self, tarjeta_id, producto_id):
        t = Tarjeta.buscar_por_id(tarjeta_id)
        if not t:
            raise ValueError("Tarjeta no encontrada")

        p = Producto.buscar_por_id(producto_id)
        if not p:
            raise ValueError("Producto no encontrado")

        if t.saldo < p.precio:
            raise ValueError("Saldo insuficiente")

        t.saldo -= p.precio
        t.guardar()

        Transaccion.crear(
            tarjeta_id=t.id,
            producto_id=p.id,
            tipo="COMPRA",
            monto=p.precio,
            descripcion=f"Compra de {p.nombre}"
        )

        return t, p
