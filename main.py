import socket
dictionary = {
	b'cat': "an animal with ears",
	b'lizard': " an animal without ears"
}
sock = socket.create_server(('192.168.254.15', 6789))
sock.listen()
conn = sock.accept()[0]
conn.send(b'Hello Eli')
conn.send(b'Look up word: ')
reply = conn.recv(4096)
word = dictionary[reply]
conn.send(str.encode(word))
input()
conn.close()