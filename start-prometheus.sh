podman run -d --name prometheus \
      -p 9090:9090 \
      --add-host=host.containers.internal:host-gateway \
      -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml:Z \
      prom/prometheus:latest
