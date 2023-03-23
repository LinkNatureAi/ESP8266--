#hello sir this code in esp8266 working
import network
import socket
from machine import ADC
import esp

esp.osdebug(None)

# Configure the ESP8266 wifi as an Access Point.
ssid = 'ESP8266'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

# Wait for the AP to be active and print its configuration.
while not ap.active():
    pass
print('Network config:', ap.ifconfig())

# Set up ADC to read from LDR sensors on pin 0 and pin 2.
ldr_pin_0 = ADC(0)
ldr_pin_2 = ADC(0)

# Set up server to listen on port 80.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Function to handle AJAX requests.
def handle_ajax_request():
    # Read values from LDR sensors.
    ldr_value_0 = ldr_pin_0.read()
    ldr_value_2 = ldr_pin_2.read()

    # Format response as JSON.
    response = '{"ldr_0": %d, "ldr_2": %d}' % (ldr_value_0, ldr_value_2)

    # Send response.
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: application/json\n')
    conn.send('Content-Length: %d\n' % len(response))
    conn.send('Connection: close\n\n')
    conn.send(response)

# Main loop.
while True:
    # Wait for incoming connection.
    conn, addr = s.accept()

    # Receive request data.
    request = conn.recv(1024)

    # Check if request is an AJAX request.
    if 'ajax' in request:
        # Handle AJAX request.
        handle_ajax_request()
    else:
        # Send HTML webpage.
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.send('<html><body style="margin: 0 auto; max-width: 800px;">' +
                  '<h1 style="font-size: 90px; color: black; text-align: center; ' +
                  'user-select: none; margin-top: 100px;">Voltage: ' +
                  '<span id="ldr_0">0</span>v</h1>' +
                  '<h1 style="font-size: 90px; color: black; text-align: center; ' +
                  'user-select: none; margin-top: 100px;">Battery: ' +
                  '<span id="ldr_2">0</span>%</h1>' +
                  '<script>setInterval(function() {' +
                  'var xhr = new XMLHttpRequest();' +
                  'xhr.open("GET", "/?ajax=1", true);' +
                  'xhr.onreadystatechange = function() {' +
                  'if (xhr.readyState == 4 && xhr.status == 200) {' +
                  'var data = JSON.parse(xhr.responseText);' +
                  'document.getElementById("ldr_0").innerHTML = data.ldr_0;' +
                  'document.getElementById("ldr_2").innerHTML = data.ldr_2;' +
                  '}' +
                  '};' +
                  'xhr.send();' +
                  '}, 100);</script>' +
                  '</body></html>')

    # Close connection.
    conn.close()

