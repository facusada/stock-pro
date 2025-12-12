from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.alquiler import Alquiler, AlquilerItem
from app.models.cliente import Cliente
from app.models.deposito import Deposito
from app.models.evento import Evento
from app.models.producto import Producto
from app.models.user import User
from app.schemas.movimiento import MovimientoCreate
from app.services.movimiento_service import create_movimiento


def run_seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Deposito).count() > 0:
            print("Seed ya ejecutado")
            return

        depositos = [
            Deposito(nombre="Depósito Central", ubicacion="Ciudad"),
            Deposito(nombre="Depósito Norte"),
            Deposito(nombre="Depósito Sur"),
        ]
        db.add_all(depositos)
        db.flush()

        productos = [
            Producto(nombre="Plato llano blanco", codigo="PL-001", unidad_medida="pieza", tipo_vajilla="Plato", material="Porcelana", estado_fisico="Excelente", stock_actual=200, stock_minimo=50, stock_disponible=200, deposito_principal_id=depositos[0].id),
            Producto(nombre="Copa de vino", codigo="CP-010", unidad_medida="pieza", tipo_vajilla="Copa", material="Vidrio", estado_fisico="Muy bueno", stock_actual=150, stock_minimo=40, stock_disponible=150, deposito_principal_id=depositos[0].id),
            Producto(nombre="Set cubiertos acero", codigo="CB-004", unidad_medida="set", tipo_vajilla="Cuchillería", material="Acero inoxidable", es_set=True, piezas_por_set=4, stock_actual=80, stock_minimo=20, stock_disponible=80, deposito_principal_id=depositos[1].id),
            Producto(nombre="Mantel premium", codigo="MT-020", unidad_medida="pieza", tipo_vajilla="Mantelería", material="Tela", stock_actual=60, stock_minimo=15, stock_disponible=60, deposito_principal_id=depositos[2].id),
        ]
        db.add_all(productos)

        clientes = [
            Cliente(nombre="Laura", apellido="Gómez", email="laura@example.com"),
            Cliente(nombre="Eventos SRL", razon_social="Eventos SRL", email="contacto@eventos.com"),
            Cliente(nombre="Martín", apellido="Rojas", email="martin@example.com"),
        ]
        db.add_all(clientes)
        db.flush()

        eventos = [
            Evento(nombre="Boda Ana y Luis", fecha_evento=date.today() + timedelta(days=20), cliente_id=clientes[0].id, estado="Confirmado"),
            Evento(nombre="Congreso Tech", fecha_evento=date.today() + timedelta(days=35), cliente_id=clientes[1].id, estado="En curso"),
        ]
        db.add_all(eventos)
        db.flush()

        alquiler = Alquiler(
            codigo="ALQ-0001",
            cliente_id=clientes[0].id,
            evento_id=eventos[0].id,
            fecha_desde=datetime.now(timezone.utc) + timedelta(days=18),
            fecha_hasta=datetime.now(timezone.utc) + timedelta(days=22),
            estado="Borrador",
            items=[
                AlquilerItem(producto_id=productos[0].id, cantidad=80, precio_unitario=1.5),
                AlquilerItem(producto_id=productos[1].id, cantidad=60, precio_unitario=2.0),
            ],
        )
        db.add(alquiler)

        create_movimiento(
            db,
            MovimientoCreate(producto_id=productos[0].id, tipo="INGRESO", cantidad=20, referencia="Compra inicial"),
            auto_commit=False,
        )

        admin = User(
            nombre="Admin",
            email="admin@example.com",
            rol="admin",
            hashed_password=get_password_hash("admin123"),
        )
        db.add(admin)

        db.commit()
        print("Seed completado")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
