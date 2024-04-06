# Raspberry Pi Relay Control

## Overview

This project provides a RESTful API to control a relay module connected to a Raspberry Pi via GPIO pins. It's built using FastAPI and runs inside a Docker container for easy deployment and scalability. The API allows you to turn the relay on, off, and toggle its state with optional delay functionality for automatic state reversal.

## Installation

### Prerequisites

- A Raspberry Pi with Docker and Docker Compose installed.
- A relay module properly connected to the Raspberry Pi's GPIO pins.

### Steps

1. **Clone the Repository**

   Clone this repository to your Raspberry Pi. If you're transferring files manually, ensure you include the `app.py`, `Dockerfile`, `requirements.txt`, and `docker-compose.yml` files.

   ```
   git clone https://github.com/Yannis4444/PiRelayControl.git
   cd PiRelayControl
   ```

2. **Configure Environment Variables**

   Edit the `docker-compose.yml` file to set the `RELAY_PIN` environment variable to the GPIO pin number you're using to control the relay.

   ```yaml
   environment:
     - RELAY_PIN=18  # Change 18 to your GPIO pin number
   ```

3. **Build and Run the Docker Container**

   Run the following command in the project directory:

   ```
   docker-compose up -d --build
   ```

   This command builds the Docker image and starts the container as defined in `docker-compose.yml`.

## Configuration

- **GPIO Pin Configuration**: To change the GPIO pin used for controlling the relay, update the `RELAY_PIN` environment variable in the `docker-compose.yml` file and restart the container.

## API Endpoints

- **Get Relay Status**: `GET /relay/status`
- **Turn Relay On**: `GET /relay/on`
- **Turn Relay Off**: `GET /relay/off`
- **Toggle Relay State**: `GET /relay/toggle`

All options except for the status support the optional `toggle_back_after` query parameter to automatically toggle back after a specified number of seconds (e.g. `/relay/on?toggle_back_after=60`).

For detailed information about the API endpoints, including request parameters and response models, visit the Swagger API documentation available at `/docs` on your Raspberry Pi's IP address and port (e.g., `http://raspberrypi.local:8080/docs`).

## GPIO Pins Overview

This project can use any GPIO pin on the Raspberry Pi for relay control. However, it's crucial to choose pins that are not reserved for special functions. Commonly used GPIO pins for such projects include GPIO17, GPIO18, GPIO27, and GPIO22, among others. Ensure the pin you choose is compatible with your relay module and properly configured in your project settings.

## Safety and Best Practices

- **Powering Relays**: Ensure your relay module is appropriately powered according to its specifications. Some relays require external power sources to handle higher voltages and currents.
- **Circuit Protection**: Consider using diodes for back-EMF protection when controlling inductive loads.
- **Testing**: Always test your setup with low power before connecting high-power loads.

## Support

For issues, suggestions, or contributions, please open an issue or pull request in the GitHub repository.