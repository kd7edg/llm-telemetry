#!/bin/bash

echo "--- Stopping LLM-telemetry Stack ---"

# 1. Stop and Remove Podman Containers
# We remove them so the --name flag in your start scripts won't conflict later.
echo "🛑 Stopping Podman containers (Grafana, Jaeger, Prometheus)..."
podman stop grafana jaeger prometheus 2>/dev/null
podman rm grafana jaeger prometheus 2>/dev/null

# 2. Kill the OpenTelemetry Collector
# This targets the binary name used in your start-otel.sh script.
echo "🛑 Shutting down OTel Collector..."
sudo pkill -9 -f "otelcol-contrib"

# 3. Stop Ollama Service
# Using systemctl prevents the service manager from automatically restarting the process.
echo "🛑 Shutting down Ollama server via systemctl..."
sudo systemctl stop ollama

# 4. Final Cleanup
# Ensures any 'nohup' processes for OTel are fully terminated.
# Redundant ollama pkill removed to allow systemctl to handle cleanup.
sudo pkill -9 -f "otelcol-contrib"

echo "--- Cleanup Complete ---"

# 5. Verification
# Runs your existing health check to confirm everything is down.
if [ -f "./check_services.py" ]; then
    echo "🔍 Running health check to verify shutdown..."
    python3 check_services.py
fi