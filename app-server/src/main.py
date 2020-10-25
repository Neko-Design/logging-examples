
# 'How to Log' Code Example
# Server Applicaton
# Copyright (c) 2020 Ewen McCahon
# https://cloudengineer.com.au

# Import Dependencies
import logging
import requests
from flask import Flask, jsonify, request

# Define Application
app = Flask(__name__)

# Define Constants
API_HOST  = "app-downstream-server"
API_PORT  = "80"
API_PROTO = "http"

# Configure Logging
logging.basicConfig(level=logging.DEBUG)

# API Request Wrapper
def make_request(path, method="GET", data=None, headers=None):
    api_url = f"{API_PROTO}://{API_HOST}:{API_PORT}{path}"
    logging.info(f"Sending Request to Web Service: ({method}) {api_url}")
    response = requests.request(method, api_url, json=data, headers=headers)
    response.raise_for_status()
    logging.info(f"Received Response from Web Service: {response.status_code}")
    return response

# Wrapper to Handle 'Business Logic'
def get_options(option_keys):
    logging.debug(f"Requesting Options: {option_keys}")
    try:
        response = make_request("/options", method="POST", data={"options": option_keys})
        options = response.json()['options']
        return {
            "success": True,
            "options": options
        }
    except requests.ConnectionError as error:
        logging.error(f"Connection Error Requesting Options: {error}")
        return {"success": False}
    except requests.HTTPError as error:
        logging.error(f"Bad Response from Options Service: {error}")
        return {"success": False}

@app.route('/')
def index():
    return jsonify({
        "message": "Server Application is Running"
    })

# Define Basic Web Service Call
# In a real application this would service some function,
# but here we are just calling our example options service
# and sending back the response, or an error if required.
@app.route("/list")
def get_list():
    options = get_options(["service-username", "service_password"])
    # If we didnt get options back, return an error
    if not options["success"]:
        return jsonify({
            "success": False,
            "message": "Unable to Service Request",
            "code": "api-500"
        }), 500
    # If we did get options back, in the real world we'd use them
    # for something, but here we will just send them back in a list
    return jsonify({
        "success": True,
        "list": options,
        "message": "List has been generated"
    })

# Define a Healthcheck
# https://tools.ietf.org/id/draft-inadarei-api-health-check-01.html
@app.route('/health')
def healthcheck():
    logging.info("Responding to Healthcheck Request")
    return jsonify({
        "description": "Server Application is Running",
        "status": "pass"
    })