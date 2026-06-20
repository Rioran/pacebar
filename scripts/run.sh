#!/usr/bin/env bash
# Run Meet Control from source (Linux/macOS).
set -e
cd "$(dirname "$0")/.."
uv run meet-control
