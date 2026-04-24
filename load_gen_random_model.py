import time
import random
import requests

# The URL where your FastAPI app is running
API_URL = "http://localhost:8000/infer"

PROMPTS = [
    "Explain quantum entanglement like I'm five.",
    "Write a Python script to scrape a website.",
    "What are the benefits of a Mediterranean diet?",
    "Summarize the plot of Inception.",
    "How do I fix a leaky faucet?",
    "Write a poem about a lonely robot on Mars.",
    "What is the capital of Kazakhstan?",
    "Explain the difference between SQL and NoSQL.",
    "Give me a 7-day workout plan for beginners.",
    "How does photosynthesis work?",
    "Write a short story about a time traveler who forgets their luggage.",
    "What are the best practices for secure passwords?",
    "Explain the theory of relativity.",
    "How do I bake a sourdough bread?",
    "What is the history of the Great Wall of China?",
    "Write a professional email asking for a salary raise.",
    "What are the main causes of climate change?",
    "Explain the concept of 'observability' in software.",
    "How do I grow organic tomatoes in Florida?",
    "What is the purpose of a blockchain?",
    "Write a script for a 30-second commercial about coffee.",
    "What are the top 5 tourist attractions in Tokyo?",
    "How do I meditate for the first time?",
    "Explain the role of a Digital Architect.",
    "What is the best way to learn a new language?",
    "Write a review for a fictional futuristic smartphone.",
    "How does a jet engine work?",
    "What are the different types of cloud computing?",
    "Explain the significance of the Magna Carta.",
    "How do I create a budget in Excel?",
    "Write a formal invitation to a wedding.",
    "What is the difference between a virus and bacteria?",
    "Explain the impact of the Industrial Revolution.",
    "How do I change a car tire?",
    "What are the key features of the Fedora operating system?",
    "Write a bedtime story for a toddler about a brave duck.",
    "How does the stock market work?",
    "What are the pros and cons of remote work?",
    "Explain the basic rules of chess.",
    "How do I make a classic Margherita pizza?",
    "What is the philosophy of Stoicism?",
    "Write a cover letter for a Senior Software Engineer position.",
    "How do I set up a smart home system?",
    "What is the importance of biodiversity?",
    "Explain how a 3D printer works.",
    "What are the common symptoms of a cold?",
    "How do I train a puppy to sit?",
    "Write a dialogue between two trees in a forest.",
    "What is the function of the human heart?",
    "Explain the concept of 'agentic AI'."
]

MODELS = ["llama3", "mistral", "phi3"]
USER_IDS = ["user_123", "user_456", "user_789", "admin_01"]
TEMPLATES = ["default-v1", "creative-v2", "concise-v1"]

def run_load_generator(iterations=100):
    print(f"🚀 Starting Multi-Model Load Generator: Sending {iterations} requests to {API_URL}...")
    
    with requests.Session() as session:
        for i in range(iterations):
            prompt = random.choice(PROMPTS)
            model = random.choice(MODELS)
            user_id = random.choice(USER_IDS)
            template = random.choice(TEMPLATES)
            
            print(f"\n[{i+1}/{iterations}] Model: {model} | Prompt: {prompt[:50]}...")
            
            try:
                params = {
                    "prompt": prompt,
                    "user_id": user_id,
                    "template": template,
                    "model": model  
                }
                
                response = session.post(API_URL, params=params, timeout=180.0)
                response.raise_for_status()
                
                data = response.json()
                print(f"✅ Success! Response received ({len(data.get('response', ''))} chars)")
                
            except Exception as e:
                print(f"❌ Error during API request: {e}")
            
            # Realistic delay for Grafana metrics
            delay = random.randint(5, 45)
            print(f"⏳ Waiting {delay} seconds...")
            time.sleep(delay)

if __name__ == "__main__":
    run_load_generator()