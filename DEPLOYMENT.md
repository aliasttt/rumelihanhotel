# Docker Deployment

## Local/VPS setup

1. Copy env file:

```bash
cp .env.example .env
```

2. Edit `.env`:

```bash
nano .env
```

Set:

- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `POSTGRES_PASSWORD`
- `SERVER_IP` or your real domain

3. Build and run:

```bash
docker compose up -d --build
```

4. Create admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

5. Seed default hotel content once, if this is a fresh server:

```bash
docker compose exec web python manage.py seed_hotel
```

6. Open:

```text
http://SERVER_IP/tr/
http://SERVER_IP/admin/
```

## Useful commands

```bash
docker compose logs -f web
docker compose logs -f nginx
docker compose exec web python manage.py seed_hotel
docker compose exec web python manage.py collectstatic --noinput
docker compose down
docker compose up -d --build
```

## Persistent data

- PostgreSQL data is stored in Docker volume `postgres_data`.
- Uploaded media is bind-mounted from `./media`.
- Collected static files are stored in Docker volume `staticfiles`.

## Database

The Docker setup uses PostgreSQL 16. Django connects to the `db` service with these env vars:

```env
POSTGRES_DB=rumelihan
POSTGRES_USER=rumelihan
POSTGRES_PASSWORD=change-this-postgres-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

To open a database shell:

```bash
docker compose exec db psql -U rumelihan -d rumelihan
```

## HTTPS

This compose file serves HTTP on port `80`. For HTTPS, put Cloudflare in front of the server or add Certbot/Caddy later.
