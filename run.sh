#!/usr/bin/env bash
# Запуск визуализации «Случайный путь» (создаёт venv при первом запуске).
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -d venv ]]; then
  python3 -m venv venv
fi
# shellcheck source=/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
python main.py
