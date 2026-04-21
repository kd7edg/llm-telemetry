#!/bin/bash

# Navigate to the project directory to ensure relative paths work
cd /home/julio/Projects/llm-telemetry/

echo "--- Starting LLM-telemetry Stack ---"

# 1. Start Infrastructure (Containers)
echo "🚀 Starting Prometheus..."
./start-prometheus.sh [cite: 188-193]

echo "🚀 Starting Jaeger..."
./start-jaeger.sh [cite: 185-187]

echo "🚀 Starting Grafana..."
./start-grafana.sh [cite: 194-199]

# Give containers a moment to initialize networking
sleep 2

# 2. Start the Telemetry Pipe
# Uses the updated path for the config file [cite: 56-92]
echo "🚀 Starting OTel Collector..."
nohup otelcol-contrib \
    --config=/home/julio/Projects/llm-telemetry/otel-config.yaml \
    > /home/julio/Projects/llm-telemetry/otel.log 2>&1 &

# 3. Start the Inference Engine
# Sets the ROCm override for the 7900 XT [cite: 110]
echo "🚀 Starting Ollama (AMD ROCm)..."
export OLLAMA_HOST=0.0.0.0
export HSA_OVERRIDE_GFX_VERSION=11.0.0 [cite: 105, 110]
nohup ollama serve > /home/julio/Projects/llm-telemetry/ollama.log 2>&1 &

# 4. Wait and Verify
echo "⏳ Waiting for services to warm up..."
sleep 5

if [ -f "./check_services.py" ]; then
    python3 check_services.py
fi

echo "--- Stack is LIVE ---"
echo "Grafana: http://localhost:3000" [cite: 209]
echo "Jaeger:  http://localhost:16686" [cite: 207]