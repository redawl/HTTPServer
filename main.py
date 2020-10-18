#includes
import socket
import threading

def get_file_type(file):
	ret = "text"
	extension = file.split(".")[1]
	if(extension == "html"):
		ret = "text/html; charset=UTF-8"
	elif(extension == "ico"):
		ret = "image/x-icon"
	elif(extension == "css"):
		ret = "text/css; charset=UTF-8"
	else:
		ret = "text; charset=UTF-8"

	return ret

def check_if_forbidden(file):
	updir = len(file.split(".."))
	downdir = len(file.split("/"))
	if(downdir / updir < 2):
		raise ValueError()

#This function will be run for every client that connects
def for_each_client(sock, conn, web_directory):
	reply = b'none'
	reply = conn.recv(4096)
	reply_raw = str(reply)[2:-1]
	requests = reply_raw.split("\\r\\n")
	reply_parsed = requests[0].split(" ")
	print("COMMAND: " + reply_parsed[0] + '\n')
	try:
		check_if_forbidden(reply_parsed[1])
		if(reply_parsed[1] != "/"):
			print(web_directory + reply_parsed[1])
		else:
			reply_parsed[1] = "/index.html"

		file = open(web_directory + reply_parsed[1], "r")
		extension = get_file_type(reply_parsed[1])
		conn.send(reply_parsed[2].encode() + b" 200 " + b"OK\r\n")
		conn.send(b"Content-Type: " + extension.encode() + b"\r\n")
		conn.send(b"\r\n")
		conn.send(file.read().encode())
	except IOError:
		conn.send(reply_parsed[2].encode() + b" 404 " + b"Not Found")
		conn.send(b"\r\n")
		conn.send(b"Sorry we don't have that file!")
	except ValueError:
		conn.send(reply_parsed[2].encode() + b" 403 " + b"Forbidden")
		conn.send(b"\r\n")
		conn.send(reply_parsed[1].encode() + b" is forbidden!")

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
