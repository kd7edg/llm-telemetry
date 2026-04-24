#!/bin/bash

# Navigate to project root regardless of where script is called from
cd "$(dirname "$0")/.."

CONTAINER_NAME="jaeger"

case "$1" in
  start)
    echo "🚀 Starting Jaeger..."
    podman run -d --name $CONTAINER_NAME \
      -e JAEGER_UI_CONFIG='{"theme": "dark"}' \
      -p 16686:16686 \
      -p 4319:4317 \
      jaegertracing/all-in-one:latest
    echo "✅ Jaeger started"
    echo "   UI:        http://localhost:16686"
    echo "   OTLP gRPC: http://localhost:4319"
    ;;

  stop)
    echo "🛑 Stopping Jaeger..."
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    echo "✅ Jaeger stopped and removed"
    ;;

  restart)
    echo "🔄 Restarting Jaeger..."
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    podman run -d --name $CONTAINER_NAME \
      -e JAEGER_UI_CONFIG='{"theme": "dark"}' \
      -p 16686:16686 \
      -p 4319:4317 \
      jaegertracing/all-in-one:latest
    echo "✅ Jaeger restarted"
    echo "   UI:        http://localhost:16686"
    echo "   OTLP gRPC: http://localhost:4319"
    ;;

  status)
    echo "📊 Jaeger status:"
    podman ps -a --filter name=$CONTAINER_NAME
    ;;

  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac