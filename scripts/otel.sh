#!/bin/bash

# Navigate to project root regardless of where script is called from
cd "$(dirname "$0")/.."

PROJECT_DIR="$(pwd)"
CONFIG="$PROJECT_DIR/otel-config.yaml"
LOG="$PROJECT_DIR/otel.log"
PID_FILE="$PROJECT_DIR/otel.pid"

case "$1" in
  start)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "⚠️  OTel Collector is already running (PID $(cat $PID_FILE))"
      exit 1
    fi
    echo "🚀 Starting OTel Collector..."
    nohup otelcol-contrib --config="$CONFIG" > "$LOG" 2>&1 &
    echo $! > "$PID_FILE"
    echo "✅ OTel Collector started (PID $(cat $PID_FILE))"
    echo "   Logs: $LOG"
    ;;

  stop)
    if [ ! -f "$PID_FILE" ]; then
      echo "⚠️  PID file not found. Is OTel Collector running?"
      exit 1
    fi
    echo "🛑 Stopping OTel Collector (PID $(cat $PID_FILE))..."
    kill $(cat "$PID_FILE")
    rm "$PID_FILE"
    echo "✅ OTel Collector stopped"
    ;;

  restart)
    echo "🔄 Restarting OTel Collector..."
    $0 stop
    sleep 1
    $0 start
    ;;

  status)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "✅ OTel Collector is running (PID $(cat $PID_FILE))"
    else
      echo "🛑 OTel Collector is not running"
    fi
    ;;

  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac