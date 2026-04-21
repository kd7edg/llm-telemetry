import httpx
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource  # <--- New Import
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
import time

# 1. Define who this service is
resource = Resource(attributes={
    "service.name": "LLM-Telemetry",          # This shows up in Jaeger
    "service.version": "1.0.0",
    "deployment.environment": "local-dev"
})

# 2. Setup the TracerProvider with that resource
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Setup Metric Exporting to the Collector
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Create a 'Meter' for your Oculum service
meter = metrics.get_meter(__name__)

# Define the specific counters for cost tracking
input_token_counter = meter.create_counter(
    "gen_ai.usage.input_tokens", 
    unit="1", 
    description="Number of input tokens"
)
output_token_counter = meter.create_counter(
    "gen_ai.usage.output_tokens", 
    unit="1", 
    description="Number of output tokens"
)

# Create a Histogram for latency (unit is seconds)
generation_latency_histogram = meter.create_histogram(
    "gen_ai.generation.duration",
    unit="s",
    description="Time taken by the GPU to generate the full response"
)

# Add a Console Exporter so you can see if the trace is even being generated locally
console_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(console_processor)

# 3. Instrument HTTPX
HTTPXClientInstrumentor().instrument()

def ask_ai(prompt,model_name="llama3"):
    with tracer.start_as_current_span("ollama_generation") as span:
        # 1. Start a local timer for absolute end-to-end check
        start_time = time.perf_counter()

        span.set_attribute("gen_ai.request.model", model_name)
        span.set_attribute("ai.prompt", prompt)
        with httpx.Client() as client:
            response = client.post(
                "http://localhost:11434/api/generate",
                json={"model": model_name, "prompt": prompt, "stream": False},
                timeout=180.0 # Increased timeout for LLM generation
            )

            # 2. Calculate the total wall-clock time
            end_time = time.perf_counter()
            total_latency_s = end_time - start_time

            data = response.json()
            result = data.get("response")

            # Extract internal GPU timing from Ollama (converted to seconds)
            gpu_duration_s = data.get("total_duration", 0) / 1e9
            
            # 3. Record both metrics for comparison in Grafana
            # This shows pure GPU time
            generation_latency_histogram.record(gpu_duration_s, {"model": model_name, "type": "gpu_pure"})
            
            # This shows the full time including overhead
            generation_latency_histogram.record(total_latency_s, {"model": model_name, "type": "end_to_end"})

            # Extract Token Usage (Semantic Conventions)
            prompt_tokens = data.get("prompt_eval_count", 0)
            completion_tokens = data.get("eval_count", 0)

            # NEW: Record the metrics numerically
            input_token_counter.add(prompt_tokens, {"model": model_name})
            output_token_counter.add(completion_tokens, {"model": model_name})
            
            # Set OTel attributes for cost calculation
            span.set_attribute("ai.response_length", len(result))
            span.set_attribute("gen_ai.usage.input_tokens", prompt_tokens)
            span.set_attribute("gen_ai.usage.output_tokens", completion_tokens)
            span.set_attribute("gen_ai.request.model", model_name)
            span.set_attribute("gen_ai.duration.gpu", gpu_duration_s)
            span.set_attribute("gen_ai.duration.total", total_latency_s)
            
            return result

if __name__ == "__main__":
    print("LLM-Telemetry: Sending prompt to Radeon 7900 XT...")
    output = ask_ai("Explain why observability is key for local AI.")
    print(f"\nAI Response: {output}")
    provider.shutdown()