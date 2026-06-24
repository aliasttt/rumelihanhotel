#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "${SEED_ON_START:-0}" = "1" ]; then
  python manage.py seed_hotel
fi

exec "$@"
