#!/usr/bin/env bash
set -euo pipefail

# Move to the directory containing this script (repo root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if pytest -s
then
  echo "All tests passed"
  exit 0
fi

#pytest -s 