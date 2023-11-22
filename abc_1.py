import requests
import socket
import re

# URL, port, and API key provided by MetricFire
metricfire_url = "e38ac701.carbon.hostedgraphite.com"
metricfire_port = 2003
metricfire_api_key = "a80345a7-7f76-48b4-95c4-987dbf2aa2c8"

# Fetch metrics from localhost:9104 (MySQL Exporter)
exporter_url = 'http://localhost:9104/metrics'
response = requests.get(exporter_url)

if response.status_code == 200:
    metrics_data = response.text  # Metrics data fetched from MySQL Exporter
    mysql_metrics = [line for line in response.text.split('\n') if line.startswith('mysql_')]
    print(f"Size of Metrics: {len(mysql_metrics)}")
    # Processing each line
    for line in mysql_metrics:
        parts = line.split(' ')
        metric_part = parts[0]
        value = parts[1]
        
        # Extracting metric name and labels
        metric_name_and_labels = metric_part.split('{')
        metric_name = metric_name_and_labels[0]
        #print(f"Metric Name: {metric_name}")
        #print(f"Value: {value}")
        
        # Establish a socket connection and send data to MetricFire
        conn = socket.create_connection((metricfire_url, metricfire_port))
        data_to_send = f"{metricfire_api_key}.{metric_name} {value}\n"
        conn.send(data_to_send.encode())
        conn.close()
        print("Metrics sent to MetricFire successfully!")
else:
    print(f"Failed to fetch metrics from MySQL Exporter. Status code: {response.status_code}")