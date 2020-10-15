#includes
import socket
import threading

#This function will be run for every client that connects
def for_each_client(sock, conn, dictionary):
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
		file = open("./www" + reply_parsed[1], "r")
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

#This will hold all the dictionary definitions
dictionary = {
	b'GET cat': "ANSWER An animal with ears",
	b'GET lizard': "ANSWER An animal without ears"
}

#This block of code handles the new clients and passes control to for_each_client()
sock = socket.create_server(('192.168.0.16', 6789))
while(1):
	sock.listen(10)
	conn = sock.accept()[0]
	print('Client Connected')
	new_thread = threading.Thread(None, for_each_client, None, (sock, conn, dictionary))
	new_thread.start()
