"""create core tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2024-05-05 00:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_create_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "depositos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("ubicacion", sa.String(length=255), nullable=True),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    )

    op.create_table(
        "clientes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("apellido", sa.String(length=255), nullable=True),
        sa.Column("razon_social", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True, unique=True),
        sa.Column("telefono", sa.String(length=50), nullable=True),
        sa.Column("direccion", sa.String(length=255), nullable=True),
        sa.Column("notas", sa.Text(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("rol", sa.String(length=50), nullable=False, server_default="operador"),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "eventos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("fecha_evento", sa.Date(), nullable=False),
        sa.Column("hora_evento", sa.Time(), nullable=True),
        sa.Column("direccion", sa.String(length=255), nullable=True),
        sa.Column("notas", sa.Text(), nullable=True),
        sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("clientes.id"), nullable=False),
        sa.Column("estado", sa.String(length=50), nullable=False, server_default="Pendiente"),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    )

    op.create_table(
        "productos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("codigo", sa.String(length=100), nullable=False),
        sa.Column("categoria", sa.String(length=255), nullable=True),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("unidad_medida", sa.String(length=50), nullable=False),
        sa.Column("tipo_vajilla", sa.String(length=50), nullable=False),
        sa.Column("material", sa.String(length=50), nullable=False),
        sa.Column("color", sa.String(length=50), nullable=True),
        sa.Column("estado_fisico", sa.String(length=50), nullable=False, server_default="Excelente"),
        sa.Column("es_set", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("piezas_por_set", sa.Integer(), nullable=True),
        sa.Column("stock_actual", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("stock_minimo", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("stock_rentado", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("stock_disponible", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("deposito_principal_id", sa.Integer(), sa.ForeignKey("depositos.id"), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
        sa.Column("fecha_actualizacion", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
        sa.UniqueConstraint("codigo", name="uq_productos_codigo"),
    )
    op.create_index("ix_productos_codigo", "productos", ["codigo"], unique=True)

    op.create_table(
        "alquileres",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("codigo", sa.String(length=50), nullable=False),
        sa.Column("cliente_id", sa.Integer(), sa.ForeignKey("clientes.id"), nullable=False),
        sa.Column("evento_id", sa.Integer(), sa.ForeignKey("eventos.id"), nullable=True),
        sa.Column("fecha_desde", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fecha_hasta", sa.DateTime(timezone=True), nullable=False),
        sa.Column("estado", sa.String(length=50), nullable=False, server_default="Borrador"),
        sa.Column("notas", sa.Text(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
        sa.UniqueConstraint("codigo", name="uq_alquiler_codigo"),
    )
    op.create_index("ix_alquileres_codigo", "alquileres", ["codigo"], unique=True)

    op.create_table(
        "alquiler_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("alquiler_id", sa.Integer(), sa.ForeignKey("alquileres.id", ondelete="CASCADE"), nullable=False),
        sa.Column("producto_id", sa.Integer(), sa.ForeignKey("productos.id"), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("precio_unitario", sa.Numeric(10, 2), nullable=True),
        sa.Column("observaciones", sa.Text(), nullable=True),
    )

    op.create_table(
        "movimientos_stock",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("producto_id", sa.Integer(), sa.ForeignKey("productos.id"), nullable=False),
        sa.Column("fecha", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
        sa.Column("tipo", sa.String(length=20), nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("deposito_origen_id", sa.Integer(), sa.ForeignKey("depositos.id"), nullable=True),
        sa.Column("deposito_destino_id", sa.Integer(), sa.ForeignKey("depositos.id"), nullable=True),
        sa.Column("referencia", sa.String(length=255), nullable=True),
        sa.Column("observaciones", sa.Text(), nullable=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("movimientos_stock")
    op.drop_table("alquiler_items")
    op.drop_index("ix_alquileres_codigo", table_name="alquileres")
    op.drop_table("alquileres")
    op.drop_index("ix_productos_codigo", table_name="productos")
    op.drop_table("productos")
    op.drop_table("eventos")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("clientes")
    op.drop_table("depositos")
