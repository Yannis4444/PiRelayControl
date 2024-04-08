import os
from typing import Optional

from fastapi import FastAPI, Query
import RPi.GPIO as GPIO
import asyncio
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Raspberry Pi Relay Control",
    description="This is a RESTful API designed to control a relay connected to a Raspberry Pi via GPIO pins. "
                "It allows for turning the relay on, off, and toggling its state with optional automatic "
                "toggling back after a specified duration. Visit https://github.com/Yannis4444/PiRelayControl for more information.",
    version="1.0.0",
)

# GPIO setup
GPIO.setmode(GPIO.BCM)
relay_pin = int(os.getenv('RELAY_PIN'))
GPIO.setup(relay_pin, GPIO.OUT)

toggle_task: Optional[asyncio.Task] = None  # Task for handling delayed toggle


class RelayResponse(BaseModel):
    message: str


class RelayStatusResponse(BaseModel):
    on: bool  # True if the relay is on, False if off


async def toggle_relay_state_delay(toggle_delay: int):
    await asyncio.sleep(toggle_delay)
    current_state = GPIO.input(relay_pin)
    GPIO.output(relay_pin, not current_state)
    state_msg = "on" if not current_state else "off"
    logger.info(f"Relay auto-toggled to {state_msg}")


def cancel_existing_task():
    global toggle_task
    if toggle_task and not toggle_task.done():
        toggle_task.cancel()
        logger.info("Existing toggle task canceled")


@app.get("/relay/status", response_model=RelayStatusResponse, tags=["Relay Control"], summary="Get Relay Status")
async def get_relay_status():
    current_state = GPIO.input(relay_pin)
    return {"on": bool(current_state)}


@app.get("/relay/on", response_model=RelayResponse, tags=["Relay Control"])
async def turn_relay_on(
        toggle_off_delay: int = Query(None, alias="toggle_off_delay", description="Time in seconds to automatically toggle the relay state back off. Optional.")
):
    global toggle_task
    cancel_existing_task()
    GPIO.output(relay_pin, GPIO.HIGH)
    logger.info("Relay turned on")
    if toggle_off_delay:
        toggle_task = asyncio.create_task(toggle_relay_state_delay(toggle_off_delay))
    return {"message": "Relay turned on"}


@app.get("/relay/off", response_model=RelayResponse, tags=["Relay Control"])
async def turn_relay_off(
        toggle_on_delay: int = Query(None, alias="toggle_on_delay", description="Time in seconds to automatically toggle the relay state back on. Optional.")
):
    global toggle_task
    cancel_existing_task()
    GPIO.output(relay_pin, GPIO.LOW)
    logger.info("Relay turned off")
    if toggle_on_delay:
        toggle_task = asyncio.create_task(toggle_relay_state_delay(toggle_on_delay))
    return {"message": "Relay turned off"}


@app.get("/relay/toggle", response_model=RelayResponse, tags=["Relay Control"])
async def toggle_relay(
        toggle_on_delay: int = Query(None, alias="toggle_on_delay", description="Time in seconds to automatically toggle the relay state back on when toggled off. Optional."),
        toggle_off_delay: int = Query(None, alias="toggle_off_delay", description="Time in seconds to automatically toggle the relay state back off when toggled on. Optional.")
):
    global toggle_task
    cancel_existing_task()
    current_state = GPIO.input(relay_pin)
    GPIO.output(relay_pin, not current_state)
    new_state_msg = "on" if not current_state else "off"
    logger.info(f"Relay toggled to {new_state_msg}")
    if current_state and toggle_off_delay:
        toggle_task = asyncio.create_task(toggle_relay_state_delay(toggle_off_delay))
    elif not current_state and toggle_on_delay:
        toggle_task = asyncio.create_task(toggle_relay_state_delay(toggle_on_delay))
    return {"message": f"Relay toggled to {new_state_msg}"}


@app.on_event("shutdown")
def shutdown_event():
    GPIO.cleanup()  # Clean up
    logger.info("GPIO cleanup performed")
