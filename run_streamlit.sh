#!/bin/sh
set -e
# $PORT 가 비어 있거나 STREAMLIT_SERVER_PORT="" 이면: Invalid value for '--server.port': '' is not a valid integer
PORT="${PORT:-8080}"
export PORT
export STREAMLIT_SERVER_PORT="$PORT"
exec streamlit run streamlit_app.py \
  --server.port="$PORT" \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --browser.gatherUsageStats=false
