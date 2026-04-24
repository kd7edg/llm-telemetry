#!/bin/bash

# Navigate to project root regardless of where script is called from
cd "$(dirname "$0")/.."

PROJECT_DIR="$(pwd)"
LOG="$PROJECT_DIR/ollama.log"
PID_FILE="$PROJECT_DIR/ollama.pid"

export OLLAMA_HOST=0.0.0.0
export HSA_OVERRIDE_GFX_VERSION=11.0.0

case "$1" in
  start)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "⚠️  Ollama is already running (PID $(cat $PID_FILE))"
      exit 1
    fi
    echo "🚀 Starting Ollama..."
    nohup ollama serve > "$LOG" 2>&1 &
    echo $! > "$PID_FILE"
    echo "✅ Ollama started (PID $(cat $PID_FILE))"
    echo "   Logs: $LOG"
    # Uncomment to warm up the 7900 XT after starting
    # echo "🔥 Warming up GPU..."
    # ollama run llama3 "warm up"
    ;;

  stop)
    if [ ! -f "$PID_FILE" ]; then
      echo "⚠️  PID file not found. Is Ollama running?"
      exit 1
    fi
    echo "🛑 Stopping Ollama (PID $(cat $PID_FILE))..."
    kill $(cat "$PID_FILE")
    rm "$PID_FILE"
    echo "✅ Ollama stopped"
    ;;

  restart)
    echo "🔄 Restarting Ollama..."
    $0 stop
    sleep 1
    $0 start
    ;;

  status)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "✅ Ollama is running (PID $(cat $PID_FILE))"
    else
      echo "🛑 Ollama is not running"
    fi
    ;;

  *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac