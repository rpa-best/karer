# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Logistics management system for tracking invoices, orders, drivers, and vehicles. Integrates with 1C (1С) accounting software via HTTP REST API. Two user roles: **manager** (creates invoices/orders) and **logist** (handles delivery, updates order status).

## Architecture

Full-stack monorepo:
- `backend/` — Django 4.2 + DRF, ASGI via uvicorn, Channels for WebSocket, Celery for async tasks
- `app/` — Nuxt 3 + Vue 3 + PrimeVue + TailwindCSS
- Infrastructure: PostgreSQL, Redis (broker + channel layer), Celery Beat for scheduled sync

### Backend Django apps
| App | Purpose |
|-----|---------|
| `oauth` | Custom User model (manager/logist roles), JWT auth (SimpleJWT) + Token auth |
| `invoice` | Invoice and Order models — core business logic |
| `onec` | 1C integration: Organization, Specification, Nomenclature, Price, Balance, Car, Driver, Sender |
| `notification` | WebSocket notifications via Django Channels |
| `career` | External API for drivers (read/patch Orders via TokenAuthentication) |
| `contrib` | Shared utilities: custom filters, managers, parsers, expressions |

### Data flow
- **1C → DB:** `onec.tasks.sync_db` (Celery Beat) pulls master data from all `Sender` URLs → populates local DB
- **DB → 1C:** `post_save` signal on `Order` calls `onec.tasks.send_order_onec(instance.pk)` directly (not via `.delay()`) to push the order to 1C

### Key model relationships
```
Sender → Organization → Specification → (used in Invoice)
Invoice → Order → Car, Driver, Nomenclature
Order.invoice.org.sender  ← used to determine which 1C base to send invoice to
```

### Frontend structure
- `services/utils.ts` — base `Api` class (axios wrapper with JWT refresh + toast), `CRUDService`/`ReadOnlyService`
- `store/` — Pinia stores (`user`, `loader`, `notifications`)
- `composables.ts` — shared refs (e.g. `token`)
- `permissions.ts` — route guard helpers (`isManager`, `isLogist`)
- `hooks/onec/` — TanStack Query hooks for 1C data (read-only, cached)
- `plugins/` — loaded in order: route guards → misc → axios Api → TanStack Query
- `i18n/` — translations in `ru.json`, `uz.json`; prefix-based routing (`/ru/`, `/uz/`), Russian is default

### Frontend pages
| Page | File | Access |
|------|------|--------|
| Dashboard (invoice list) | `pages/index.vue` | All |
| Login | `pages/login.vue` | Public |
| Cars | `pages/car.vue` | Manager |
| Drivers | `pages/driver.vue` | Manager |

## Commands

### Local Docker
```bash
docker compose up -d
docker compose up career_backend career_redis career_postgres  # backend only
```
Backend: `:8000`, Frontend: `:4000`

### Backend (inside container or venv)
```bash
python3 manage.py migrate
python3 manage.py runserver
python3 -m py_compile <file.py>   # syntax check after edits
celery -A backend worker -l info
celery -A backend beat -l info
```

### Frontend
```bash
cd app && npm install
npm run dev        # :4000
npm run build && npm run preview
```

### Production (server)
```bash
cd /var/www/karer
docker compose up -d
docker compose restart career_backend career_celery career_celery_beat  # после изменений в backend/
docker compose build career_frontend && docker compose up -d career_frontend  # после изменений в app/
docker compose logs -f career_backend  # смотреть логи
```

## Production Server

- **Host:** `147.45.250.43`, SSH root (использовать paramiko из Python, expect недоступен на Windows)
- **Project path:** `/var/www/karer/`
- **Containers:** `career_backend`, `career_frontend`, `career_celery`, `career_celery_beat`, `career_redis`, `career_postgres`
- **ВАЖНО:** На сервере несколько проектов — трогать только `karer`, остальные не трогать

### Деплой файла на сервер (через paramiko)
```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('147.45.250.43', username='root', password='...', timeout=10)
sftp = client.open_sftp()
sftp.put('local/path.py', '/var/www/karer/backend/...')
sftp.close()
```

### Запуск кода в контейнере
```bash
docker cp /tmp/script.py career_backend:/tmp/script.py
docker exec career_backend python3 /tmp/script.py
```
Внутри скриптов обязательно добавлять в начало:
```python
import sys; sys.path.insert(0, '/app')
import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()
```

## Key Env Vars

### backend/.env
```
DEBUG=1
SECRET_KEY=...
POSTGRES_DB=career
POSTGRES_USER=career
POSTGRES_PASSWORD=career
POSTGRES_HOST=career_postgres
POSTGRES_PORT=5432
REDIS_HOST=career_redis
ONEC_HOST=http://<1c-host>:<port>
ONEC_USERNAME=<логин>
ONEC_PASSWORD=***REMOVED***
```

### app/.env
```
REDIS_HOST=career_redis
NUXT_APP_BACKEND_HOST=http://localhost:8000/api
NUXT_APP_WS_HOST=ws://localhost:8000
```

## API & Auth

- REST API: `/api/` prefix, Swagger: `/api/docs/`
- Frontend: **JWT** (access + refresh в `token` composable), auto-refresh на 401
- `career` app: **DRF TokenAuthentication** (отдельный API для водителей)
- Роли: backend (`oauth/permissions.py`) + frontend route guards (`permissions.ts`)

## 1C Integration

### Сenders в БД
| Sender | URL (для data) | URL (для invoice) |
|--------|---------------|-------------------|
| Ресурс | `/resource/hs/career/data` | `/resource/hs/career/invoice` |
| Неруд-Трейд | `/accounting/hs/career/data` | `/accounting/hs/career/invoice` |

Full URL = `ONEC_HOST + sender.url`, Basic Auth (ONEC_USERNAME / ONEC_PASSWORD из .env).

### send_order_onec (backend/onec/tasks.py)
Путь к invoice-эндпоинту определяется динамически из sender организации заказа:
```python
sender = order.invoice.org.sender
invoice_path = sender.url.rsplit('/', 1)[0] + '/invoice'
url = HOST + invoice_path
```
**Важно:** функция пропускается если `settings.DEBUG = True` (интеграция отключена локально).

### Текущий статус 1C API (на 2026-06-04)
- GET `/resource/hs/career/data` и `/accounting/hs/career/data` — работают, синхронизация ок
- POST `/resource/hs/career/invoice` и `/accounting/hs/career/invoice` — возвращают 500 "Обработчик запроса вернул некорректное значение"
- Это баг на стороне 1С в обработчике invoice. Нужно передать 1С-разработчику тело запроса и попросить проверить журнал регистрации 1С
- Путь `/accounting_copy/hs/career/invoice` (был захардкожен ранее) — несуществующий, таймаутит

### Тело запроса для invoice (POST)
```json
{
  "XML_ID": "UUID заказа",
  "DATE": "YYYY-MM-DD HH:MM:SS",
  "SPECIFICATION_ID": "UUID спецификации",
  "SHIPPER_ID": "",
  "CONSIGNEE_ID": "UUID организации",
  "CARRIER_ID": "",
  "PACKAGE": "",
  "DELIVERY": 1,
  "COMMENT": "текст",
  "DRIVER_ID": "UUID водителя",
  "VEHICLE_ID": "UUID машины",
  "DOCUMENTS": "",
  "TRANS_INFO": "",
  "ITEMS": [{"ITEM_ID": "UUID номенклатуры", "QUANTITY": 10.0}]
}
```
DELIVERY: 1=Самовывоз, 2=Собственная доставка, 3=Евротранс, 4=БАРС, 6=Сторонние

## WebSocket Notifications

- Backend: `notification/consumers.py`, channel group `notification_{user_id}`
- Frontend: `components/notifications/websocket.ts`, подключается через `NUXT_APP_WS_HOST`
- Отправить: `notification.consumers.send_notification(notification_instance)`

## Known Bugs Fixed

### Double JSON serialization (onec/tasks.py)
`requests.post(url, json=json.dumps(data))` было неверно — `json=` уже сериализует. Исправлено на `json=data`.

### Frontend 404 при логине (app/store/user.ts)
`loginUrl()` использовал полный URL (`http://host/path`) в параметре `next`. Исправлено: использует `useRoute().fullPath` (относительный путь) + `encodeURIComponent`.

### Хардкод /accounting_copy/ в send_order_onec
Исправлено: путь теперь берётся динамически из `order.invoice.org.sender.url`.
