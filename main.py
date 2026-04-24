import httpx
import time
import uvicorn
from fastapi import FastAPI
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
#from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor # Changed this to debug
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

# 1. Setup Resource and Providers
resource = Resource(attributes={
    "service.name": "llm-telemetry-agent",  # Matches the blog's naming convention
    "deployment.environment": "local-dev"
})

# Tracing Setup
provider = TracerProvider(resource=resource)
# processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
processor = SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("llm-telemetry.agent")

# Metrics Setup
metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True))
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("llm-telemetry.metrics")

# Define Counters
input_token_counter = meter.create_counter("gen_ai.usage.input_tokens", unit="1")
output_token_counter = meter.create_counter("gen_ai.usage.output_tokens", unit="1")
latency_histogram = meter.create_histogram("gen_ai.generation.duration", unit="s")

# 2. Initialize FastAPI
app = FastAPI()

# 3. Apply Auto-Instrumentation
# This links incoming HTTP requests to outgoing LLM calls
FastAPIInstrumentor().instrument_app(app)
HTTPXClientInstrumentor().instrument()

@app.post("/infer")
async def run_inference(prompt: str, user_id: str, template: str = "default-v1", model: str = "llama3"):
    # The 'with' block creates a span that tracks this specific request
    with tracer.start_as_current_span("llm-telemetry.inference") as span:
        # Attach high-cardinality attributes for better filtering
        span.set_attribute("user.id", user_id)
        span.set_attribute("prompt.template.name", template)
        span.set_attribute("app.version", "1.0.0")

        start_time = time.perf_counter()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=180.0
            )
            
            data = response.json()
            gpu_duration_s = data.get("total_duration", 0) / 1e9
            
            # Record metrics
            input_tokens = data.get("prompt_eval_count", 0)
            output_tokens = data.get("eval_count", 0)
            
            input_token_counter.add(input_tokens, {"model": model})
            output_token_counter.add(output_tokens, {"model": model})
            latency_histogram.record(gpu_duration_s, {"model": model})

            # Add an OTel Event for the completed inference
            span.add_event("inference.complete", {"tokens_generated": output_tokens})

            return {"response": data.get("response")}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)