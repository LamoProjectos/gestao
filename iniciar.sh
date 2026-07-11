#!/bin/bash
# LamoProjectos - Iniciar Sistema
echo "=== LamoProjectos ==="

source "$(dirname "$0")/.venv/bin/activate"

# Servidor Django (gestão)
cd "$(dirname "$0")/gestao"
echo "A iniciar gestão em http://localhost:8000"
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Servidor frontend (site)
cd "$(dirname "$0")/frontend"
echo "A iniciar site em http://localhost:3000"
python -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "=============================================="
echo "  SITE:     http://localhost:3000"
echo "  GESTÃO:   http://localhost:8000"
echo "  LOGIN:    admin / 56510  |  eng / 1234"
echo "=============================================="
echo ""
echo "Prima Ctrl+C para parar"

trap "kill $DJANGO_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
