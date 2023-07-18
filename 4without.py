# WELCOME
try:
  import usocket as socket
except:
  import socket

import machine
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = ''
password = ''

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

# ESP32 GPIO 2
relay = machine.Pin(2, machine.Pin.OUT)

def web_page():
    if relay.value() == 1:
        relay_state = ''
    else:
        relay_state = 'checked'
        
    html = """
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0,user-scalable=yes">
            <style>   
                body {
                    font-family: Arial; 
                    text-align: center; 
                    margin: 0px auto; 
                    padding-top: 30px; 
                    user-select: none;
                }
                .switch {
                    position: relative;
                    display: inline-block;
                    width: 120px;
                    height: 68px
                }
                .switch input {
                    display: none
                }
                .slider {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-color: #353535;
                    border-radius: 34px
                }
                .slider:before {
                    position: absolute;
                    content: "";
                    height: 52px;
                    width: 52px;
                    left: 8px;
                    bottom: 8px;
                    background-color: #fff;
                    -webkit-transition: .2s;
                    transition: .2s;
                    border-radius: 68px
                }
                input:checked+.slider {
                    background-color: #bf21f3
                }
                input:checked+.slider:before {
                    -webkit-transform: translateX(52px);
                    -ms-transform: translateX(52px);
                    transform: translateX(52px)
                }
            </style>
            <script>
                function toggleCheckbox(element) {
                    var xhr = new XMLHttpRequest();
                    if (element.checked) {
                        xhr.open("GET", "/?relay=on", true);
                    } else {
                        xhr.open("GET", "/?relay=off", true);
                    }
                    xhr.send();
                }
            </script>
        </head>
        <body>
            <h1>WELCOME</h1>
            <label class="switch">
                <input type="checkbox" onchange="toggleCheckbox(this)" %s>
                <span class="slider"></span>
            </label>
        </body>
    </html>
    """ % (relay_state)
    
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    relay_on = request.find('/?relay=on')
    relay_off = request.find('/?relay=off')
    if relay_on == 6:
      print('RELAY ON')
      relay.value(1)
    if relay_off == 6:
      print('RELAY OFF')
      relay.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
