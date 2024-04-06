import os

from fastapi import FastAPI, Query
import RPi.GPIO as GPIO
import asyncio
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# GPIO setup
GPIO.setmode(GPIO.BCM)
relay_pin = int(os.getenv('RELAY_PIN'))
GPIO.setup(relay_pin, GPIO.OUT)

toggle_task: asyncio.Task = None  # Task for handling delayed toggle


class RelayResponse(BaseModel):
    message: str


async def toggle_relay_state_after(toggle_back_after: int):
    await asyncio.sleep(toggle_back_after)
    current_state = GPIO.input(relay_pin)
    GPIO.output(relay_pin, not current_state)
    state_msg = "on" if not current_state else "off"
    logger.info(f"Relay auto-toggled to {state_msg}")


def cancel_existing_task():
    global toggle_task
    if toggle_task and not toggle_task.done():
        toggle_task.cancel()
        logger.info("Existing toggle task canceled")


@app.get("/relay/on", response_model=RelayResponse, tags=["Relay Control"])
async def turn_relay_on(toggle_back_after: int = Query(None, alias="toggle_back_after", description="Time in seconds to automatically toggle the relay state back. Optional.")):
    global toggle_task
    cancel_existing_task()
    GPIO.output(relay_pin, GPIO.HIGH)
    logger.info("Relay turned on")
    if toggle_back_after:
        toggle_task = asyncio.create_task(toggle_relay_state_after(toggle_back_after))
    return {"message": "Relay turned on"}


@app.get("/relay/off", response_model=RelayResponse, tags=["Relay Control"])
async def turn_relay_off(toggle_back_after: int = Query(None, alias="toggle_back_after", description="Time in seconds to automatically toggle the relay state back. Optional.")):
    global toggle_task
    cancel_existing_task()
    GPIO.output(relay_pin, GPIO.LOW)
    logger.info("Relay turned off")
    if toggle_back_after:
        toggle_task = asyncio.create_task(toggle_relay_state_after(toggle_back_after))
    return {"message": "Relay turned off"}


@app.get("/relay/toggle", response_model=RelayResponse, tags=["Relay Control"])
async def toggle_relay(toggle_back_after: int = Query(None, alias="toggle_back_after", description="Time in seconds to automatically toggle the relay state back. Optional.")):
    global toggle_task
    cancel_existing_task()
    current_state = GPIO.input(relay_pin)
    GPIO.output(relay_pin, not current_state)
    new_state_msg = "on" if not current_state else "off"
    logger.info(f"Relay toggled to {new_state_msg}")
    if toggle_back_after:
        toggle_task = asyncio.create_task(toggle_relay_state_after(toggle_back_after))
    return {"message": f"Relay toggled to {new_state_msg}"}


@app.on_event("shutdown")
def shutdown_event():
    GPIO.cleanup()  # Clean up
    logger.info("GPIO cleanup performed")
