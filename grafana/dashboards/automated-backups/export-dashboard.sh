# This creates a variable with the current timestamp
TIMESTAMP=$(date +"%Y%m%dT%H%M")

curl -H "Authorization: Bearer ${GRAFANA_TOKEN}" \
     http://localhost:3000/api/dashboards/uid/adcqt47 \
     > my_dashboard_${TIMESTAMP}.json
