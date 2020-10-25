
# 'How to Log' Code Example
# Downstream Server Applicaton
# Copyright (c) 2020 Ewen McCahon
# https://cloudengineer.com.au

# Import Dependencies
import logging
import random
from flask import Flask, jsonify, request
from time import sleep

# Define Constants
ERROR_THRESHOLD   = 25
TIMEOUT_THRESHOLD = 50

# Define Application
app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return jsonify({
        "message": "Downstream Server Application is Running"
    })

# This downstream service is acting as an example config
# service, handling a single 'options' endpoint. In the 
# real world this would be backed by a data store, but here
# we can just respond with random data.
# There is a 50% chance of success, 25% chance of a timeout,
# and 25% chance of an error
@app.route("/options", methods=['POST'])
def get_options():
    request_number = random.randint(0,100)
    if (request_number <= ERROR_THRESHOLD):
        # Send an Error for some responses
        logging.warn("Sending error due to request number. This simulates a failed request.")
        return jsonify({
            "success": False,
            "message": "Unable to Service Request",
            "code": "api-500"
        }), 500
    elif (ERROR_THRESHOLD < request_number < TIMEOUT_THRESHOLD):
        # Timeout or take a while for others
        logging.warn(f"Sleeping ({request_number}) due to request number. This simulates a slow call.")
        sleep(request_number)
    # Send back a valid response
    logging.warn("Proceeding with request due to request number.")
    request_data = request.get_json(force=True)
    if "options" not in request_data:
        logging.error("Required field 'options' not in request. Cannot proceed.")
        return jsonify({
            "success": False,
            "message": "Required field 'options' missing from request",
            "code": "api-400"
        }), 400
    request_options = request_data['options']
    logging.debug(f"Processing request for options: [{request_options}]")
    response_data = {}
    for option in request_options:
        response_data[option] = request_number
    return jsonify({
        "success": True,
        "message": "Options have been generated",
        "options": response_data,
        "code": "api-200"
    })

# Define a Healthcheck
# https://tools.ietf.org/id/draft-inadarei-api-health-check-01.html
@app.route('/health')
def healthcheck():
    logging.info("Responding to Healthcheck Request")
    return jsonify({
        "description": "Downstream Server Application is Running",
        "status": "pass"
    })