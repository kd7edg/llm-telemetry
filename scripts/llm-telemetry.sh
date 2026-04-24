#!/bin/bash

# Navigate to project root regardless of where script is called from
cd "$(dirname "$0")/.."

SCRIPTS_DIR="$(pwd)/scripts"

case "$1" in
  start)
    echo "--- Starting LLM-telemetry Stack ---"
    echo ""

    # 1. Start Infrastructure (Containers)
    bash "$SCRIPTS_DIR/prometheus.sh" start
    bash "$SCRIPTS_DIR/jaeger.sh" start
    bash "$SCRIPTS_DIR/grafana.sh" start

    # Give containers a moment to initialize networking
    echo "⏳ Waiting for containers to initialize..."
    sleep 2

    # 2. Start the Telemetry Pipe
    bash "$SCRIPTS_DIR/otel.sh" start

    # 3. Start the Inference Engine
    bash "$SCRIPTS_DIR/ollama.sh" start

    # 4. Wait and Verify
    echo ""
    echo "⏳ Waiting for services to warm up..."
    sleep 5

    bash "$SCRIPTS_DIR/check_services.sh"

    echo ""
    echo "--- Stack is LIVE ---"
    echo "   Grafana:  http://localhost:3000"
    echo "   Jaeger:   http://localhost:16686"
    echo "   Prometheus: http://localhost:9090"
    ;;

  stop)
    echo "--- Stopping LLM-telemetry Stack ---"
    echo ""

    bash "$SCRIPTS_DIR/ollama.sh" stop
    bash "$SCRIPTS_DIR/otel.sh" stop
    bash "$SCRIPTS_DIR/grafana.sh" stop
    bash "$SCRIPTS_DIR/jaeger.sh" stop
    bash "$SCRIPTS_DIR/prometheus.sh" stop

    echo ""
    echo "--- Stack is DOWN ---"
    ;;

  *)
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac