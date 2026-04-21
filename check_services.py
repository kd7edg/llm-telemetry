import socket
import subprocess

def check_port(name, port, host="127.0.0.1"):
    """Checks if a specific port is open on the host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex((host, port))
        if result == 0:
            print(f"✅ {name:15} is RUNNING on port {port}")
            return True
        else:
            print(f"❌ {name:15} is NOT RESPONDING on port {port}")
            return False

def check_process(name, command):
    """Checks if a specific process is visible in the system process list."""
    try:
        output = subprocess.check_output(["pgrep", "-f", command])
        if output:
            print(f"✅ {name:15} process is ACTIVE")
            return True
    except subprocess.CalledProcessError:
        print(f"❌ {name:15} process is NOT FOUND")
        return False


def main():
    print("--- LLM-telemetry Stack Health Check ---")
    
    # 1. OTel Collector
    # Checks port 4317 and the binary name
    otel_ok = check_port("OTel Collector", 4317) and check_process("OTel Collector", "otelcol-contrib")
    
    # 2. Prometheus
    # Checks port 9090 and the container/process
    prom_ok = check_port("Prometheus", 9090) and check_process("Prometheus", "prometheus")
    
    # 3. Jaeger
    # Checks port 16686 and the container/process
    jaeger_ok = check_port("Jaeger UI", 16686) and check_process("Jaeger", "jaeger")
    
    # 4. Ollama
    # Checks port 11434 and the local serve process
    ollama_ok = check_port("Ollama API", 11434) and check_process("Ollama", "ollama")

    print("\n--- Summary ---")
    if all([otel_ok, prom_ok, jaeger_ok, ollama_ok]):
        print("🚀 All systems go! You are ready to run the load generator.")
    else:
        print("⚠️  Some services are down. Please check the '❌' items above.")

if __name__ == "__main__":
    main()