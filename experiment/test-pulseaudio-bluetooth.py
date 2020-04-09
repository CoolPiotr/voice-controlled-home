#!/usr/bin/python3

# Developed using Python 3.8.2

import pulsectl
import bluetooth


blu = bluetooth.BluetoothSocket(bluetooth.L2CAP)
blu.setblocking(True)

timeout = 10
while timeout > 0:
	try:
		blu.connect()
		timeout = -1
	except bluetooth.btcommon.BluetoothError:
		time.sleep(1)
		timeout -= 1
		print("Waiting for connection...")
		continue

if timeout == 0:
	print("Could not connect to server.")
else:
	print("Successfully connected")



"""
# synchronous discovery of available Bluetooth devices (finds my phone if it's on the Bluetooth page)
nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
	print(bluetooth.lookup_name(bdaddr))
"""


"""
#nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
#print (nearby_devices)
server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
port = 0x1001

server_sock.bind(("", port))
server_sock.listen(1)

client_sock, address = server_sock.accept()
print("Accepted connection from", address)
data = client_sock.recv(1024)
print("Data received:", str(data))

while data:
	client_sock.send("Echo =>", str(data))
	data = client_sock.recv(1024)
	print("Data received:", str(data))

client_sock.close()
server_sock.close()
"""

'''
with pulsectl.Pulse("test-junk") as pulse:
	print(pulse.sink_list())
	print(pulse.sink_list()[0].proplist)
	print()
	print(pulse.source_list())
	for thing in pulse.source_list():
		if "device.bus" in thing.proplist:
			print ("Bluetooth device '" + thing.proplist["device.description"] + "' is playing (exists to Pulse)")
			#print (thing.proplist)
		else:
			print (thing.proplist)

'''
