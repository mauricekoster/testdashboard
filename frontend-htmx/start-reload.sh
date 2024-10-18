#! /usr/bin/env sh
set -e

exec fastapi dev --host 0.0.0.0 --port 80
