#includes
import socket
import threading

#This function will be run for every client that connects
def for_each_client(sock, conn, dictionary):
	conn.send(b'Hello Eli\r\n')
	reply = b'none'
	while(reply != b'q'):
		conn.send(b'Look up word: ')
		reply = conn.recv(4096)
		try:
			word = dictionary[reply]
			conn.send(str.encode(word) + b"\r\n")
		except:
			if(reply != b'q'):
				conn.send(b"ERROR cant find " + reply + b"\r\n")
		conn.recv(4096)
	conn.close()

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
	new_thread = threading.Thread(None, for_each_client, None, (sock, conn, dictionary))
	new_thread.start()
