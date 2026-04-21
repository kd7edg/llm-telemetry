import time
import random
import httpx
from main import ask_ai, input_token_counter, output_token_counter, generation_latency_histogram

# List of models to compare
MODELS = ["llama3", "mistral", "phi3"]

# Selection of prompts from the previous 50-prompt list for the comparison test
PROMPTS = [
    "Explain quantum entanglement like I'm five.",
    "Explain the theory of relativity.",
    "What is the difference between SQL and NoSQL?",
    "How does a jet engine work?",
    "Explain the concept of 'observability' in software.",
    "What are the key features of the Fedora operating system?",
    "Explain the impact of the Industrial Revolution.",
    "What is the philosophy of Stoicism?",
    "Explain how a 3D printer works.",
    "Explain the concept of 'agentic AI'."
]

def run_comparison_test(iterations=5):
    print(f"🚀 Starting Model Comparison Test: Running {iterations} prompts across {len(MODELS)} models...")
    
    for i in range(iterations):
        prompt = random.choice(PROMPTS)
        print(f"\n[{i+1}/{iterations}] Prompt: {prompt}")
        print("-" * 50)
        
        for model in MODELS:
            print(f"🤖 Testing Model: {model}...", end=" ", flush=True)
            try:
                # Capture timing for console feedback (main.py records to OTel)
                start = time.perf_counter()
                response = ask_ai(prompt, model_name=model)
                end = time.perf_counter()
                
                duration = end - start
                print(f"✅ Success! ({duration:.2f}s)")
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        # Add a small delay between prompt groups to keep the Grafana timeline clean
        if i < iterations - 1:
            delay = 10
            print(f"\n⏳ Waiting {delay}s before next prompt set...")
            time.sleep(delay)

if __name__ == "__main__":
    # Ensure this script only runs if called directly
    run_comparison_test(iterations=5)