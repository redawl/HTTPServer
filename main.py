#includes
import socket
import threading

#This function will be run for every client that connects
def for_each_client(sock, conn, web_directory):
	reply = b'none'
	reply = conn.recv(4096)
	reply_raw = str(reply)[2:-1]
	requests = reply_raw.split("\\r\\n")
	reply_parsed = requests[0].split(" ")
	print('METHOD: ' + reply_parsed[0] + '\n')
	print('RESOURCE: ' + reply_parsed[1] + '\n')
	print('VERSION: ' + reply_parsed[2] + '\n')
	for i in range(len(requests) - 1):
		print(requests[i + 1])

	try:
		file = open(web_directory + reply_parsed[1], "r")
		conn.send(reply_parsed[2].encode() + b"200" + b"OK")
		conn.send(b"\r\n")
		conn.send(file.read().encode())
	except:
		print('Requested File Not Found')
		conn.send(reply_parsed[2].encode() + b"404" + b"Not Found")
		conn.send(b"\r\n")
		conn.send(b"Sorry we don't have that file!")

	conn.close()
	print('Client Disconnected')

#Read Configuration from config.txt
cfgFile = open("config.txt", "r")
cfg = cfgFile.read()
cfg_parsed = cfg.split("\n")
print(cfg_parsed)
host = cfg_parsed[0].split(" ")[1]
port = cfg_parsed[1].split(" ")[1]
web_directory = cfg_parsed[2].split(" ")[1]

#This block of code handles the new clients and passes control to for_each_client()
sock = socket.create_server((host, int(port)))
while(1):
	sock.listen(10)
	conn = sock.accept()[0]
	print('Client Connected')
	new_thread = threading.Thread(None, for_each_client, None, (sock, conn, web_directory))
	new_thread.start()
