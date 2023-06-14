import machine
import time

# Set up the LED pin
led_pin = machine.Pin(12, machine.Pin.OUT)

# Set up the serial communication
uart = machine.UART(0, baudrate=115200)

# Loop forever
while True:
    # Turn the LED on
    led_pin.on()
    # Print a message to the serial monitor
    uart.write('LED ON\n'.encode())
    # Wait for 1 second
    time.sleep(5)
    # Turn the LED off
    led_pin.off()
    # Print a message to the serial monitor
    uart.write('LED OFF_esp8266_main_py\n'.encode())
    # Wait for 1 second
    time.sleep(1)
