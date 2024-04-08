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

Based on the provided OpenAPI JSON, your REST interface for "Raspberry Pi Relay Control" offers endpoints for controlling a relay connected to a Raspberry Pi through GPIO pins. This RESTful API enables users to get the current status of the relay, turn it on or off, and toggle its state, with optional automatic reversal after a set duration. Here's a short overview of each endpoint:

1. **Get Relay Status (`/relay/status`)**
   - **Method**: GET
   - **Description**: Retrieves the current status of the relay, indicating whether it is on or off.
   - **Response**: The current state of the relay as a boolean value (`true` for on, `false` for off) in JSON format.

2. **Turn Relay On (`/relay/on`)**
   - **Method**: GET
   - **Description**: Activates the relay, optionally allowing for an automatic turn-off after a specified delay.
   - **Parameters**: An optional `toggle_off_delay` query parameter can be provided to specify the time in seconds after which the relay should automatically turn off.

3. **Turn Relay Off (`/relay/off`)**
   - **Method**: GET
   - **Description**: Deactivates the relay, with an option to automatically turn it back on after a specified delay.
   - **Parameters**: An optional `toggle_on_delay` query parameter can be included to set the time in seconds for the relay to automatically turn back on.

4. **Toggle Relay (`/relay/toggle`)**
   - **Method**: GET
   - **Description**: Toggles the relay's current state from on to off or vice versa. It also supports automatic re-toggling based on provided delay parameters for both states.
   - **Parameters**: Optional `toggle_on_delay` and `toggle_off_delay` query parameters can be used to define the time in seconds for automatic re-toggling when the relay is turned off and on, respectively.

For detailed information about the API endpoints, including request parameters and response models, visit the Swagger API documentation available at `/docs` on your Raspberry Pi's IP address and port (e.g., `http://raspberrypi.local:8080/docs`).

## GPIO Pins Overview

This project can use any GPIO pin on the Raspberry Pi for relay control. However, it's crucial to choose pins that are not reserved for special functions. Commonly used GPIO pins for such projects include GPIO17, GPIO18, GPIO27, and GPIO22, among others. Ensure the pin you choose is compatible with your relay module and properly configured in your project settings.

## Safety and Best Practices

- **Powering Relays**: Ensure your relay module is appropriately powered according to its specifications. Some relays require external power sources to handle higher voltages and currents.
- **Circuit Protection**: Consider using diodes for back-EMF protection when controlling inductive loads.
- **Testing**: Always test your setup with low power before connecting high-power loads.

## Support

For issues, suggestions, or contributions, please open an issue or pull request in the GitHub repository.