#!/usr/bin/env bash
# Публикация на GitHub (один раз). Требуется: gh auth login
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v gh >/dev/null 2>&1; then
  echo "Установите GitHub CLI: brew install gh"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Войдите в GitHub: gh auth login"
  gh auth login
fi

REPO_NAME="${1:-sluchaynyy-put}"
gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
echo ""
echo "Готово. Добавьте ссылку в таблицу «Репозитории»:"
gh repo view --web 2>/dev/null || gh repo view --json url -q .url
