# Career

## Production start (Docker)

1. Copy env templates:
   - `cp backend/.env.example backend/.env`
   - `cp app/.env.example app/.env`
2. Fill real values in `backend/.env` and `app/.env`:
   - `SECRET_KEY`, `POSTGRES_PASSWORD`
   - `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`
   - `NUXT_APP_BACKEND_HOST`
   - optional: `ONEC_*`, SMTP variables
3. Build and run:
   - `docker compose -f docker-compose.prod.yml up -d --build`
4. Check status and logs:
   - `docker compose -f docker-compose.prod.yml ps`
   - `docker compose -f docker-compose.prod.yml logs -f career_backend`