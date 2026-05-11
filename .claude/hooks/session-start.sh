#!/bin/bash
# SessionStart hook: installs Python deps and dev tools so Claude Code on the web
# can run linters, tests, and the pipeline in a fresh sandbox.
set -euo pipefail

# Only run in the Claude Code on the web environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

REPO_ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
REQS="$REPO_ROOT/code/requirements.txt"
PIP_FLAGS="--break-system-packages --no-build-isolation --disable-pip-version-check -q --root-user-action=ignore"

echo "[session-start] bootstrapping pip/setuptools/wheel"
# setuptools<81 keeps pkg_resources, required by legacy build scripts (e.g. fuzzywuzzy)
pip install --break-system-packages --ignore-installed --disable-pip-version-check -q --root-user-action=ignore \
  "setuptools<81" wheel pip

if [ -f "$REQS" ]; then
  # cx_Oracle requires Oracle Instant Client and is unused in the default pipeline.
  FILTERED_REQS="$(mktemp)"
  trap 'rm -f "$FILTERED_REQS"' EXIT
  grep -vE '^\s*cx_Oracle' "$REQS" > "$FILTERED_REQS"

  echo "[session-start] installing project requirements"
  pip install $PIP_FLAGS -r "$FILTERED_REQS"
fi

echo "[session-start] installing dev tools (ruff, pytest)"
pip install $PIP_FLAGS ruff pytest

# Make `from src...` imports work without cd code/.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PYTHONPATH=\"$REPO_ROOT/code:\${PYTHONPATH:-}\"" >> "$CLAUDE_ENV_FILE"
fi

echo "[session-start] done"
