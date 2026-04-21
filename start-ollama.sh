export OLLAMA_HOST=0.0.0.0
export HSA_OVERRIDE_GFX_VERSION=11.0.0
nohup ollama serve > ~/Projects/oculum/ollama.log 2>&1 &

# Warm up the 7900 XT
# ollama run llama3 "warm up"
