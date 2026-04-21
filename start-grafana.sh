podman run -d \
  --name=grafana \
  --net=host \
  -v grafana-storage:/var/lib/grafana:Z \
  grafana/grafana:latest