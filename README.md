# Logging Examples Code
Code from my 'How to Log' Articles

The purpose of this repo is to provide a hands-on example application which readers can work with while going through my 'How to Log' series of articles. This application doesn't actually do anything, it just simulates a fairly standard multi-tiered application in a convenient, docker-compose based environment that can be easily run on a normal computer.

This is an example python 'ecosystem in a bottle' with a client, a server, and a downstream server. When the client makes a request, the server receives that request and calls the downstream for additional information. The downstream service includes logic to randomly succeed, timeout, and return an error to help demonstrate the various possible error scenarios logging can help with.

## Client Application

A basic python CLI application that makes a call to the server application every 5 seconds. First it calls the `/health` endpoint to make sure it's running, then it calls the `/list` endpoint to get an example piece of data.

## Server Application

The server application for our example CLI, handles a single `/list` endpoint which calls the downstream application service for some example configuration items via a POST with JSON body to the `/options` endpoint. If it gets a successful response, it builds a response object and sends it back to the CLI as JSON.

## Downstream Server Application

The downstream service for our example server application, pretending to be a sort of config endpoint. Handles a single `/options` endpoint that takes JSON POST requests and returns a dictionary of responses for each element in the request's `options` field. This call includes logic to timeout or error as configured in the constants at the top of the applications code under [app-downstream-server/src/main.py](app-downstream-server/src/main.py).

# Getting Started

To get set up to run the applications provided in this repository, install docker for your operating system from [the Docker website](https://www.docker.com/products/docker-desktop). Once installed, in the parent `logging-examples` directory, run `docker-compose up --build` to build and start the containers. You should end up with 3 containers running, from which you can see output in your terminal.

Every 5 seconds, the client application will send a request to the server, which in turn will call the downstream application. This should produce the below output if everything is working correctly:

```
app-client_1             | INFO:root:Sending Request to Web Service: (GET) http://app-server:80/health
app-server_1             | INFO:root:Responding to Healthcheck Request
app-client_1             | INFO:root:Received Response from Web Service: 200
app-client_1             | INFO:root:Web Service Status: pass
app-client_1             | INFO:root:Sending Request to Web Service: (GET) http://app-server:80/list
app-server_1             | DEBUG:root:Requesting Options: ['service-username', 'service_password']
app-server_1             | INFO:root:Sending Request to Web Service: (POST) http://app-downstream-server:80/options
app-downstream-server_1  | WARNING:root:Proceeding with request due to request number.
app-downstream-server_1  | DEBUG:root:Processing request for options: [['service-username', 'service_password']]
app-server_1             | INFO:root:Received Response from Web Service: 200
app-client_1             | INFO:root:Received Response from Web Service: 200
app-client_1             | INFO:root:Successful Response from List Service: {'list': {'options': {'service-username': 85, 'service_password': 85}, 'success': True}, 'message': 'List has been generated', 'success': True}
```