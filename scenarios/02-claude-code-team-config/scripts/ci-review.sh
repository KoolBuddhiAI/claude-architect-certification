#!/usr/bin/env bash
# Headless Claude Code review in CI — outputs structured JSON, exits non-zero on issues
# Usage: ./scripts/ci-review.sh path/to/changed_file.py

set -euo pipefail

FILE="${1:?Usage: $0 <file>}"

claude \
  --output-format json \
  --max-turns 5 \
  --no-interactive \
  "Review $FILE for correctness, security issues, and style violations.
   Output a JSON object with fields: approved (bool), issues (array of {severity, description}).
   Exit immediately after producing the JSON." \
| jq -e '.approved == true' > /dev/null

echo "Review passed: $FILE"
