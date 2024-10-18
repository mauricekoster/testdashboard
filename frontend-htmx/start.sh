#! /usr/bin/env sh
set -e

exec fastapi run --host 0.0.0.0 --port 80
