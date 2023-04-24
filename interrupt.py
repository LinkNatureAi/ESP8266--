import machine
import time

# Define GPIO pins
led = machine.Pin(2, machine.Pin.OUT)
button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

# Define interrupt handler
def interrupt_handler(pin):
    led.value(not led.value())

# Set up interrupt on button pin
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=interrupt_handler)

# Blink LED every 5 seconds
while True:
    led.value(not led.value())
    time.sleep(5)
