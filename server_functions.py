#This function gets the correct file type, and returns the Content-Type to be sent to the client
def get_file_type(file):
	ret = "text"
	extension = file.split(".")[1]
	if(extension == "html"):
		ret = "text/html; charset=UTF-8"
	elif(extension == "ico"):
		ret = "image/x-icon"
	elif(extension == "css"):
		ret = "text/css; charset=UTF-8"
	elif(extension == "jpg"):
		ret = "image/jpeg"
	else:
		ret = "text; charset=UTF-8"

	return ret

#This function makes sure the request stays in the bounds of the web directory
def check_if_forbidden(file):
	updir = len(file.split(".."))
	downdir = len(file.split("/"))
	if(updir == 0 or downdir / updir < 2):
		raise ValueError()

#This function will be run for every client that connects
def for_each_client(sock, conn, web_directory):
	reply_raw = str(conn.recv(4096))[2:-1]
	requests = reply_raw.split("\\r\\n")
	reply_parsed = requests[0].split(" ")
	METHOD = reply_parsed[0]
	RESOURCE = reply_parsed[1]
	HTTP_VERSION = reply_parsed[2]
	print("METHOD: " + METHOD + '\n')
	try:
		check_if_forbidden(RESOURCE)#Throws ValueError if resorce path is outside of web_directory
		if(RESOURCE != "/"):
			print(web_directory + RESOURCE)
		else:
			RESOURCE = "/index.html"

		file = open(web_directory + RESOURCE, "rb")#Throws IOError if file doesn't exist
		extension = get_file_type(RESOURCE)
		conn.send(HTTP_VERSION.encode() + b" 200 " + b"OK\r\n")
		conn.send(b"Content-Type: " + extension.encode() + b"\r\n")
		conn.send(b"\r\n")
		conn.send(file.read())
	except IOError:
		conn.send(HTTP_VERSION.encode() + b" 404 " + b"Not Found")
		conn.send(b"\r\n")
		conn.send(b"Sorry we don't have that file!")
	except ValueError:
		conn.send(HTTP_VERSION.encode() + b" 403 " + b"Forbidden")
		conn.send(b"\r\n")
		conn.send(RESOURCE.encode() + b" is forbidden!")

	conn.close()
	print('Client Disconnected')
