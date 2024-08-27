import requests
import json

# Define the API endpoint URL
host = '0.0.0.0'
api_url = f'http://{host}:5001/extract_fields'  # Update with your API URL

# Read the JSON file and load the content into a Python dictionary
with open('materials/input.json', 'r') as json_file:
    products = json.load(json_file)

model_name = 'LLaMA' #'CameLLM'

# Create the payload dictionary
payload = {
    'products': products,
    'model': model_name,
}

# Print the payload for verification
print(json.dumps(payload, indent=4))

# Convert the payload to JSON
payload_json = json.dumps(payload)

# Send a POST request to the API
response = requests.post(api_url, json=payload_json)

# Print the response
print("Response status code:", response.status_code)
print("Response JSON:", response.json())