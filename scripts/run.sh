#!/usr/bin/env bash
# Run PaceBar from source (Linux/macOS).
set -e
cd "$(dirname "$0")/.."
uv run pacebar
