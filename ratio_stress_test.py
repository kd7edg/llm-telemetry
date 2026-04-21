import time
from main import ask_ai

def run_stress_test():
    print("🚀 Starting Oculum Ratio Stress Test...")
    
    # 1. THE "IDEAL" RATIO (High Efficiency)
    # Very short prompt, long descriptive answer.
    print("\n[SCENARIO 1] Testing 'Very Good' Ratio (Efficient)...")
    ask_ai("Write a 300-word essay on the history of Linux.")

    # 2. THE "BLOATED" PROMPT (Negative Testing - Poor Ratio)
    # Sending massive context for a tiny answer.
    print("\n[SCENARIO 2] Testing 'Very Bad' Ratio (Negative Testing: Bloat)...")
    bloat = "This is a sentence used to bloat the input. " * 500
    prompt_bloat = f"Context: {bloat} \n\n Question: What is the word after 'sentence' in the first line?"
    ask_ai(prompt_bloat)

    # 3. THE "SYSTEMD EXPERT" (Balanced Ratio)
    # Detailed technical question with a technical answer.
    print("\n[SCENARIO 3] Testing 'Balanced' Ratio (Technical Query)...")
    ask_ai("Explain the difference between a systemd Timer and a Cron job on Fedora Silverblue.")

    # 4. THE "REPEATED BLOAT" (To spike the Grafana Red Zone)
    # We do this a few times to make sure the Prometheus average drops.
    print("\n[SCENARIO 4] Hammering the 'Bad' Ratio to trigger Grafana Thresholds...")
    for i in range(3):
        print(f"  > Sending Bloat Wave {i+1}...")
        large_file_sim = "DATA_LOG_ENTRY_ID_" + "X" * 100 + "\n"
        ask_ai(f"Analyze this log: {large_file_sim * 200} \n Summary: Give me one word: OK or FAIL.")

    print("\n✅ Stress test complete. Check your Grafana 'Input-to-Output' Panel.")

if __name__ == "__main__":
    # Ensure your OTel collector and Ollama are running!
    try:
        run_stress_test()
    except Exception as e:
        print(f"Error during test: {e}")