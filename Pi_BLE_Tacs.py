import RPi.GPIO as GPIO
from bleak import BleakClient, BleakScanner, BleakError
import asyncio
import time

# Mapping of GPIO pins to the corresponding letters (as byte strings)
BUTTON_PINS = {
    5: b'a',
    6: b'd',
    13: b'q',
    19: b'w',
    26: b'e',
    21: b'x'
}

# BLE settings
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
DEVICE_NAME = "Figproxy_Receiver"

# Debounce time (50 ms)
button_debounce_time = 0.05

async def connect_to_m5dial():
    print("Scanning for Figproxy_Receiver...")

    while True:
        try:
            device = await BleakScanner.find_device_by_name(DEVICE_NAME)
            if device:
                print(f"Found {DEVICE_NAME}, attempting to connect...")
                async with BleakClient(device) as client:
                    print(f"Connected to {DEVICE_NAME}")
                    while True:
                        await handle_inputs(client)
                        await asyncio.sleep(0.001)
        except asyncio.TimeoutError:
            print(f"Connection attempt to {DEVICE_NAME} timed out. Retrying in 2 seconds...")
            await asyncio.sleep(2)
        except BleakError as e:
            print(f"BLE error: {e}. Retrying in 2 seconds...")
            await asyncio.sleep(2)

async def handle_inputs(client):
    # Loop through each button pin and check if it's pressed
    for pin, letter in BUTTON_PINS.items():
        if GPIO.input(pin) == GPIO.LOW:
            # Wait briefly to debounce the button press
            await asyncio.sleep(button_debounce_time)
            if GPIO.input(pin) == GPIO.LOW:
                await client.write_gatt_char(CHARACTERISTIC_UUID, letter, response=True)
                print(letter.decode())
                time.sleep(0.05)  # Additional debounce delay

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # Set each button pin as input with an internal pull-up resistor
    for pin in BUTTON_PINS.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == "__main__":
    setup_gpio()
    try:
        asyncio.run(connect_to_m5dial())
    except KeyboardInterrupt:
        print("\nDisconnected.")
        GPIO.cleanup()
