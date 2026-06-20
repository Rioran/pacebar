#!/usr/bin/env bash
# Build a slimmed-down standalone binary into dist/ (Linux/macOS).
set -e
cd "$(dirname "$0")/.."
uv run --extra build pyinstaller --noconfirm --clean meet-control.spec
echo "Built: dist/meet-control"
