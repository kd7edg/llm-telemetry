podman run -d --name jaeger \
      -e JAEGER_UI_CONFIG='{"theme": "dark"}' \
      -p 16686:16686 \
      -p 4319:4317 \
      jaegertracing/all-in-one:latest
