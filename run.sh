#!/usr/bin/env bash
# Run the certification scenarios against MiniMax's Anthropic-compatible API.
#
# Usage:
#   ./run.sh            # run all scenarios
#   ./run.sh 05         # run only scenario 05
#
# Loads config from .env (copy from env.example and add your MiniMax key first).
set -euo pipefail
cd "$(dirname "$0")"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
else
  echo "No .env found. Run: cp env.example .env  and add your MiniMax API key." >&2
  exit 1
fi

PY="./.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

scenario_path() {
  case "$1" in
    01) echo "scenarios/01-customer-support-agent/main.py" ;;
    03) echo "scenarios/03-multi-agent-research/main.py" ;;
    04) echo "scenarios/04-developer-productivity/main.py" ;;
    05) echo "scenarios/05-ci-cd-automation/main.py" ;;
    06) echo "scenarios/06-structured-data-extraction/main.py" ;;
    *)  echo "" ;;
  esac
}

run_one() {
  local id="$1" path
  path="$(scenario_path "$id")"
  if [[ -z "$path" ]]; then
    echo "Unknown scenario: $id (valid: 01 03 04 05 06)" >&2
    return 2
  fi
  echo "======================================================================"
  echo ">>> Scenario $id  ($path)  model=${MODEL:-default}"
  echo "======================================================================"
  set +e
  "$PY" "$path"
  local rc=$?
  set -e
  echo "    [scenario $id exit code: $rc]"
  echo
}

if [[ $# -ge 1 ]]; then
  run_one "$1"
else
  for id in 01 03 04 05 06; do
    run_one "$id" || true
  done
fi
