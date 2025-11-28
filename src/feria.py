from tarjeta import Tarjeta
from tienda import Tienda
from producto import Producto
from transaccion import Transaccion

class Feria:
    def crear_tarjeta(self, nombre: str) -> Tarjeta:
        return Tarjeta.crear(nombre)

    def listar_tarjetas(self):
        return Tarjeta.listar_todas()

    def eliminar_tarjeta(self, tarjeta_id: int):
        Tarjeta.eliminar(tarjeta_id)

    def actualizar_nombre_tarjeta(self, tarjeta_id: int, nuevo_nombre: str):
        t = Tarjeta.buscar_por_id(tarjeta_id)
        if not t:
            raise ValueError("Tarjeta no encontrada")
        t.nombre = nuevo_nombre
        t.guardar()
        return t

    def depositar(self, tarjeta_id: int, monto: float) -> Tarjeta:
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
            descripcion="Depósito a tarjeta"
        )
        return t

    def listar_tiendas(self):
        return Tienda.listar_todas()

    def listar_productos_por_tienda(self, tienda_id: int):
        return Producto.listar_por_tienda(tienda_id)

    # --- COMPRAS ---
    def comprar(self, tarjeta_id: int, producto_id: int):
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
