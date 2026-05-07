#!/usr/bin/env bash
set -e

: "${PORT:=8000}"

exec gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:${PORT} main:app
