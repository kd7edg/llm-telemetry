#!/bin/bash

# Navigate to project root regardless of where script is called from
cd "$(dirname "$0")/.."

CONTAINER_NAME="grafana"

case "$1" in
  start)
    echo "🚀 Starting Grafana..."
    podman run -d \
      --name=$CONTAINER_NAME \
      --net=host \
      -v grafana-storage:/var/lib/grafana:Z \
      grafana/grafana:latest
    echo "✅ Grafana started on http://localhost:3000"
    echo "   Default credentials: admin / admin"
    ;;

  stop)
    echo "🛑 Stopping Grafana..."
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    echo "✅ Grafana stopped and removed"
    ;;

  restart)
    echo "🔄 Restarting Grafana..."
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    podman run -d \
      --name=$CONTAINER_NAME \
      --net=host \
      -v grafana-storage:/var/lib/grafana:Z \
      grafana/grafana:latest
    echo "✅ Grafana restarted on http://localhost:3000"
    ;;

  status)
    echo "📊 Grafana status:"
    podman ps -a --filter name=$CONTAINER_NAME
    ;;

  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac