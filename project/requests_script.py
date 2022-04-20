import requests
from datetime import datetime

# Make sure you run pip install requests

SERVER_IP = 'http://127.0.0.1'
PORT = 5000
GET_ENDPOINTS = ['read']
POST_ENDPOINTS = ['write']

# Generate base URL template
BASE_URL = f"{SERVER_IP}:{PORT}/"

for endpoint in GET_ENDPOINTS:
    URL = f"{BASE_URL}{endpoint}"
    print(f"ENDPOINT HIT: /{endpoint}")
    print(f"ABSOLUTE URL: {URL}")

    timestamp_before = datetime.now()
    # sending get request and saving the response as response object
    data = {
        'key': 'key'
    }
    r = requests.get(url=URL, json=data)
    timestamp_after = datetime.now()

    print(f"\nTime:-\nBefore: {timestamp_before}, After: {timestamp_after}")
    print(f"Time to fulfill: {timestamp_after-timestamp_before}")

    print('-------------------------------')

for endpoint in POST_ENDPOINTS:
    URL = f"{BASE_URL}{endpoint}"
    print(f"ENDPOINT HIT: /{endpoint}")
    print(f"ABSOLUTE URL: {URL}")

    # defining a params dict for the parameters to be sent to the API
    data = {
        'key': 'key',
        'value': 'value'
    }

    timestamp_before = datetime.now()
    # sending get request and saving the response as response object
    r = requests.post(url=URL, json=data)
    timestamp_after = datetime.now()

    print(f"\nTime:-\nBefore: {timestamp_before}, After: {timestamp_after}")
    print(f"Time to fulfill: {timestamp_after-timestamp_before}")

    print('-------------------------------')
