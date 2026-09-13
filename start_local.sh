#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
BRIDGE_DIR="$ROOT_DIR/whatsapp-bridge"
STOPPED=false

if [[ ! -f "$BACKEND_DIR/.env" || ! -f "$BRIDGE_DIR/.env" ]]; then
  echo "Create backend/.env and whatsapp-bridge/.env from their .env.example files first."
  exit 1
fi
if [[ ! -x "$BACKEND_DIR/.venv/bin/python3" ]]; then
  echo "Backend virtual environment is missing: $BACKEND_DIR/.venv"
  exit 1
fi
if [[ ! -d "$BRIDGE_DIR/node_modules" ]]; then
  echo "Bridge packages are missing. Run: cd whatsapp-bridge && npm install"
  exit 1
fi

cleanup() {
  if [[ "$STOPPED" == true ]]; then
    return
  fi
  STOPPED=true
  echo "Stopping chatbot services..."
  kill "${BACKEND_PID:-}" "${BRIDGE_PID:-}" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

(
  cd "$BACKEND_DIR"
  exec "$BACKEND_DIR/.venv/bin/python3" -m uvicorn app.main:app --host 127.0.0.1 --port 8010
) &
BACKEND_PID=$!

echo "Waiting for chatbot backend on http://127.0.0.1:8010 ..."
for _ in {1..20}; do
  if curl -fsS http://127.0.0.1:8010/health >/dev/null; then
    break
  fi
  sleep 1
done
if ! curl -fsS http://127.0.0.1:8010/health >/dev/null; then
  echo "Backend did not become healthy. Check its error above."
  exit 1
fi

(
  cd "$BRIDGE_DIR"
  exec npm start
) &
BRIDGE_PID=$!

wait "$BACKEND_PID" "$BRIDGE_PID"
