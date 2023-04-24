import machine
import time
import ustruct

# configure RTC with current time
rtc = machine.RTC()
rtc.datetime((2023, 4, 24, 0, 0, 0, 0, 0))

# define GPIO pin for LED
led_pin = machine.Pin(2, machine.Pin.OUT)

# define time interval for blinking in seconds
blink_interval_sec = 5

# loop to blink LED every 5 seconds
while True:
    # get current time from RTC
    (year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
    print("Current time:", year, "-", month, "-", day, " ", hours, ":", minutes, ":", seconds)

    # toggle LED every 5 seconds
    if seconds % blink_interval_sec == 0:
        led_pin.value(not led_pin.value())

    # wait for the remaining time in the interval
    time.sleep(blink_interval_sec - seconds % blink_interval_sec)
