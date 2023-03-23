import network
import socket
import machine
import time

ssid = ""
password = ""

ap_ssid = "Setup Portal"
ap_password = "mrdiy.ca"

html = """<!DOCTYPE html>
<html>
<head>
	<title>Wifi Setup</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<style>
		body {
			font-family: Arial, Helvetica, sans-serif;
			background-color: #f5f5f5;
			margin: 0;
			padding: 0;
		}

		h1 {
			font-size: 1.5rem;
			text-align: center;
			margin-top: 1.5rem;
		}

		.form {
			max-width: 400px;
			margin: 1.5rem auto;
			background-color: #fff;
			border-radius: 10px;
			padding: 1rem;
			box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
		}

		.form label,
		.form input[type="password"],
		.form input[type="text"] {
			display: block;
			width: 100%;
			margin-top: 0.5rem;
		}

		.form input[type="password"],
		.form input[type="text"] {
			padding: 0.5rem;
			font-size: 1rem;
			border: 1px solid #ccc;
			border-radius: 3px;
			background-color: #f5f5f5;
			color: #333;
		}

		.form button[type="submit"] {
			display: block;
			width: 100%;
			padding: 0.5rem;
			font-size: 1rem;
			background-color: #007bff;
			color: #fff;
			border: none;
			border-radius: 3px;
			margin-top: 1rem;
			cursor: pointer;
		}

		.error {
			color: red;
			margin-top: 0.5rem;
			font-size: 0.8rem;
		}
	</style>
</head>
<body>
	<div class="form">
		<h1>Wifi Setup</h1>
		<form method="post">
			<label for="ssid">SSID:</label>
			<input type="text" id="ssid" name="ssid" required>
			<label for="password">Password:</label>
			<input type="password" id="password" name="password" required>
			<button type="submit">Save</button>
		</form>
	</div>
</body>
</html>
"""

def connect_to_wifi():
    global ssid, password

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    if not sta_if.isconnected():
        print("Connecting to wifi...")
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            time.sleep(1)
        print("Wifi connected: ", sta_if.ifconfig())

def start_ap():
    global ap_ssid, ap_password, html

    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=ap_ssid, password=ap_password)
    print("Access Point started: ", ap_if.ifconfig())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print("Listening on port 80...")
    
    while True:
        client_sock, client_addr = s.accept()
        print("Client connected: ", client_addr)
        handle_request(client_sock)
