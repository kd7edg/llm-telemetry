#!/bin/bash

# Navigate to project root regardless of where script is called from
cd "$(dirname "$0")/.."

SCRIPTS_DIR="$(pwd)/scripts"

echo "--- LLM-telemetry Stack Health Check ---"
echo ""

bash "$SCRIPTS_DIR/prometheus.sh" status
bash "$SCRIPTS_DIR/jaeger.sh" status
bash "$SCRIPTS_DIR/grafana.sh" status
bash "$SCRIPTS_DIR/ollama.sh" status
bash "$SCRIPTS_DIR/otel.sh" status

echo ""
echo "--- Summary ---"

# Check all services by re-running status and capturing exit codes
all_ok=true

for service in otel prometheus jaeger grafana ollama; do
  bash "$SCRIPTS_DIR/$service.sh" status > /dev/null 2>&1 || all_ok=false
done

if $all_ok; then
  echo "🚀 All systems go! You are ready to run the load generator."
else
  echo "⚠️  Some services are down. Please check the items above."
fi