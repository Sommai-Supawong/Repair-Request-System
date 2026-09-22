#!/usr/bin/env bash
set -euo pipefail

python3 -m flask --app app init-db
exec python3 -m gunicorn app:app --bind "0.0.0.0:${PORT:-10000}" --workers "${WEB_CONCURRENCY:-1}" --access-logfile - --error-logfile -
