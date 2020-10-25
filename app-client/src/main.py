
# 'How to Log' Code Example
# Client Applicaton
# Copyright (c) 2020 Ewen McCahon
# https://cloudengineer.com.au

# Import Dependencies
import logging
import requests
from time import sleep

# Define Constants
API_HOST  = "app-server"
API_PORT  = "80"
API_PROTO = "http"

# Configure Logging
logging.basicConfig(level=logging.INFO)

# API Request Wrapper
def make_request(path, method="GET", data=None, headers=None):
    api_url = f"{API_PROTO}://{API_HOST}:{API_PORT}{path}"
    logging.info(f"Sending Request to Web Service: ({method}) {api_url}")
    response = requests.request(method, api_url, json=data, headers=headers)
    response.raise_for_status()
    logging.info(f"Received Response from Web Service: {response.status_code}")
    return response

# When executed directly, make a request
if __name__ == "__main__":
    while True:
        sleep(5)
        try:
            response = make_request("/health")
            logging.info(f"Web Service Status: {response.json()['status']}")
            if response.ok:
                list_response = make_request("/list")
                if list_response.ok:
                    logging.info(f"Successful Response from List Service: {list_response.json()}")
        except requests.ConnectionError as error:
            logging.error(f"Error Connecting to Web Service: {error}")
        except requests.HTTPError as error:
            logging.error(f"Bad Response from Web Service: {error}")