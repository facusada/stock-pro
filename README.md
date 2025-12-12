# Stock Backend (FastAPI)

Backend en FastAPI para gestionar inventario y alquileres de vajilla para eventos. Incluye autenticación JWT, control de stock con movimientos y panel de seguimiento.

## Requisitos

- Python 3.11+
- PostgreSQL 13+
- Herramientas CLI: `pip`, `alembic`, `uvicorn`

## Configuración rápida

1. Instalar dependencias:

   ```bash
   pip install -e .
   ```

2. Crear archivo `.env` (opcional) en la raíz:

   ```env
   DATABASE_URL=postgresql+psycopg://usuario:password@localhost:5432/stock_db
   SECRET_KEY=una_clave_segura
   ACCESS_TOKEN_EXPIRE_MINUTES=120
   ```

   Si no se define, se usarán los valores por defecto indicados en `app/core/config.py`.

3. Crear la base de datos en PostgreSQL.

## Migraciones

Aplicar las tablas iniciales con Alembic:

```bash
alembic upgrade head
```

Para generar nuevas migraciones basadas en los modelos SQLAlchemy:

```bash
alembic revision --autogenerate -m "descripcion"
```

## Datos de ejemplo (opcional)

Ejecuta el script de seed para cargar depósitos, productos, clientes, eventos y un usuario admin (`admin@example.com` / `admin123`):

```bash
python -m app.services.seed_data
```

## Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en `http://localhost:8000`. Documentación interactiva en `http://localhost:8000/docs`.

## Autenticación

- Registrar usuario: `POST /api/auth/register`
- Iniciar sesión (OAuth2 password flow): `POST /api/auth/login`
- Usar el `access_token` devuelto como `Authorization: Bearer <token>` para operaciones protegidas.

## Endpoints destacados

- `GET /api/productos` filtra por `search`, `categoria`, `tipo_vajilla`, `stock_bajo`, etc.
- `POST /api/productos` crea productos controlando stock disponible.
- `POST /api/movimientos` registra ingresos, egresos, ajustes, alquileres o devoluciones y actualiza stock.
- `POST /api/alquileres/{id}/confirmar` y `/registrar-devolucion` automatizan el movimiento de stock asociado a los pedidos.
- `GET /api/dashboard/resumen` entrega métricas clave.
- `GET /api/agenda/proximos-eventos` lista eventos próximos con sus alquileres.

### Ejemplos `curl`

Registrar usuario (temporalmente sin restricción de rol):

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Admin",
    "email": "admin@example.com",
    "password": "admin123",
    "rol": "admin"
  }'
```

Obtener token JWT:

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=admin@example.com&password=admin123'
```

Crear un producto protegido (requiere token):

```bash
curl -X POST http://localhost:8000/api/productos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Plato de postre",
    "codigo": "PL-200",
    "unidad_medida": "pieza",
    "tipo_vajilla": "Plato",
    "material": "Porcelana",
    "estado_fisico": "Excelente",
    "stock_actual": 100,
    "stock_minimo": 20,
    "deposito_principal_id": 1
  }'
```

Registrar movimiento de ingreso:

```bash
curl -X POST http://localhost:8000/api/movimientos \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "producto_id": 1,
    "tipo": "INGRESO",
    "cantidad": 25,
    "referencia": "Compra proveedor"
  }'
```

## Estructura del proyecto

```
app/
  api/            # Routers y endpoints
  core/           # Configuración y seguridad
  db/             # Base declarativa y sesión
  models/         # Modelos SQLAlchemy
  schemas/        # Modelos Pydantic
  services/       # Lógica de dominio y casos de uso
  main.py         # Punto de entrada FastAPI
alembic/          # Migraciones
```

## Próximos pasos sugeridos

- Separar permisos (admin/operador) en endpoints críticos.
- Añadir pruebas automáticas y CI.
- Integrar notificaciones para alertas de stock.
