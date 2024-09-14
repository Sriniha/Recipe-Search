from opensearchpy import OpenSearch, helpers
from opensearchpy.helpers import bulk
import json

# Connect to OpenSearch
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True,  # Enables gzip compression for request bodies
    http_auth=('admin', 'Bin2@2305'),  # Update with your credentials
    use_ssl=True,  # If you're using SSL
    verify_certs=False,
    timeout = 30,
    max_retries = 3,
    retry_on_timeout = True# Disable if you're using self-signed certificates
)

# Load the JSON file (line by line for multiple JSON objects)
actions = []
with open(r"D:\sriansh\Recipes Search Platform\epi_r_bulk.json", 'r') as f:
    for line in f:
        try:
            record = json.loads(line.strip())  # Parse each line as a separate JSON object
            actions.append({
                "_index": "epi_r_index",
                "_source": record
            })
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {line}")
            print(f"Error: {e}")

# Bulk ingest the data
if actions:
    response = helpers.bulk(client, actions)
    print("Bulk upload complete:", response)
else:
    print("No valid actions to upload.")