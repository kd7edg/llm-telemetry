import time
import random
from main import generation_latency_histogram

def simulate_latency_variance(iterations=20):
    """
    Simulates a mix of fast, normal, and spiked latency values 
    to verify that P50, P95, and P99 metrics in Grafana are working.
    """
    print(f"🚀 Starting Latency Stress Test: Injecting {iterations} data points...")
    
    models = ["llama3", "mistral", "phi3"]
    
    for i in range(iterations):
        model = random.choice(models)
        
        # 80% of the time, record "Normal" performance (1.5s - 3.0s)
        if random.random() < 0.80:
            latency = random.uniform(1.5, 3.0)
            tag = "NORMAL"
        # 15% of the time, record a "Slow" request (5.0s - 7.0s)
        elif random.random() < 0.95:
            latency = random.uniform(5.0, 7.0)
            tag = "SLOW  "
        # 5% of the time, record a massive "Spike" (12.0s - 18.0s)
        else:
            latency = random.uniform(12.0, 18.0)
            tag = "SPIKE "

        print(f"[{i+1:02d}] Model: {model:8} | Latency: {latency:5.2f}s | Type: {tag}")
        
        # Record the metric to the OTel histogram
        generation_latency_histogram.record(
            latency, 
            {"model": model, "type": "gpu_pure"}
        )
        
        # Short sleep to avoid overwhelming the collector buffer
        time.sleep(0.5)

    print("\n✅ Stress test complete. Check your 'Latency Percentiles' panel in Grafana.")
    print("You should see the P99 line pull significantly higher than the P50 line.")

if __name__ == "__main__":
    from opentelemetry import metrics
    
    simulate_latency_variance()
    
    # Force flush to ensure metrics are sent to the collector before exit
    metrics.get_meter_provider().force_flush()