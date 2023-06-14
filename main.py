import gc
import urequests as requests
import network
import uasyncio as asyncio
import machine
import time

# Set up the LED pin
led_pin = machine.Pin(12, machine.Pin.OUT)

# Set up the serial communication
uart = machine.UART(0, baudrate=115200)
# Set up the URL for the new main.py file
MAIN_SCRIPT_URL = 'https://raw.githubusercontent.com/LinkNatureAi/ESP8266/main/main.py'

# Wi-Fi credentials
SSID = "POCO X3 Pro"
PASSWORD = "1234567890"  # Connect to Wi-Fi network

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Connected to WiFi:', wlan.ifconfig())

# Check for main.py updates
async def check_for_updates():
    print('Checking for main.py updates...')
    response = requests.get(MAIN_SCRIPT_URL)
    if response.status_code == 200:
        remote_script = response.text
        with open('main.py', 'r') as f:
            local_script = f.read()
        if remote_script != local_script:
            print('New main.py available. Updating...')
            await update_main_script(remote_script)
        else:
            print('main.py is up to date.')
    else:
        print('Failed to fetch main.py:', response.status_code)

# Update the main.py script
async def update_main_script(remote_script):
    with open('main.py', 'w') as f:
        f.write(remote_script)
    print('main.py updated.')

# Main program loop
async def main():
    connect_to_wifi()
    await check_for_updates()
    # No need to perform_ota_update() here; it will be performed automatically after the main function completes

async def led_loop():
    while True:
        # Turn the LED on
        led_pin.on()
        # Print a message to the serial monitor
        uart.write('LED ON\n'.encode())
        # Wait for 1 second
        await asyncio.sleep(1)
        # Turn the LED off
        led_pin.off()
        # Print a message to the serial monitor
        uart.write('LED OFF_esp8266_main_py\n'.encode())
        # Wait for 1 second
        await asyncio.sleep(1)

# Run the event loop
async def run():
    await asyncio.gather(main(), led_loop())

# Start the program
gc.collect()
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
