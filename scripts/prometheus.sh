#!/bin/bash

# Navigate to project root regardless of where script is called from
cd "$(dirname "$0")/.."

CONTAINER_NAME="prometheus"

case "$1" in
  start)
    echo "🚀 Starting Prometheus..."
    podman run -d --name $CONTAINER_NAME \
      -p 9090:9090 \
      --add-host=host.containers.internal:host-gateway \
      -v $(pwd)/prometheus.yaml:/etc/prometheus/prometheus.yaml:Z \
      prom/prometheus:latest
    echo "✅ Prometheus started on http://localhost:9090"
    ;;

  stop)
    echo "🛑 Stopping Prometheus..."
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    echo "✅ Prometheus stopped and removed"
    ;;

  restart)
    echo "🔄 Restarting Prometheus..."
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    podman run -d --name $CONTAINER_NAME \
      -p 9090:9090 \
      --add-host=host.containers.internal:host-gateway \
      -v $(pwd)/prometheus.yaml:/etc/prometheus/prometheus.yaml:Z \
      prom/prometheus:latest
    echo "✅ Prometheus restarted on http://localhost:9090"
    ;;

  status)
    echo "📊 Prometheus status:"
    podman ps -a --filter name=$CONTAINER_NAME
    ;;

  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac