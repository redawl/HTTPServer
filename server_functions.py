from os.path import splitext

# This function gets the correct file type, and returns the Content-Type to be sent to the client
def get_file_type(file, cfg):
    ret = "text"
    extension = splitext(file)[1]
    
    try:
        return cfg.get("file_types", extension)
    except:
        return "text"


# This function makes sure the request stays in the bounds of the web directory
def check_if_forbidden(file):
    updir = len(file.split(".."))
    sanitized = ""
    for i in range(len(file) - 1):
        if file[i] == "/":
            if file[i + 1] != "/":
                sanitized += file[i]
        else:
            sanitized += file[i]
    sanitized += file[len(file) - 1]
    downdir = len(sanitized.split("/"))
    if updir == 0 or downdir / updir < 2:
        raise ValueError(403)


def verify_method(method, cfg):
    is_supported = True
    try:
        is_supported = cfg.getboolean("methods", method) 
    except:
        raise ValueError(400)

    if is_supported == False:
        raise ValueError(405)


def verify_http_version(http_version):
    if http_version != "HTTP/1.1":
        raise ValueError(505)


# This function will be run for every client that connects
def for_each_client(sock, conn, web_directory, cfg):
    reply_raw = str(conn.recv(8192))[2:-1]
    if reply_raw == "":  # checks if client disconnected without sending request
        print("Client Disconnected")
        conn.close()
        return None
    elif len(reply_raw) > 4096:
        conn.send(b"HTTP/1.1" + b" 413 Payload Too Large")
        conn.send(b"\r\n")
        conn.send(b"Request was too large for server to handle!")
        conn.close()
        return None
    requests = reply_raw.split("\\r\\n")
    reply_parsed = requests[0].split(" ")

    if len(reply_parsed) < 3:
        conn.send(b"HTTP/1.1" + b" 400 Bad Request\r\n")
        conn.send(b"Unreadable Request!\r\n")
        conn.close()
        return None
    method = reply_parsed[0]
    resource = reply_parsed[1]
    http_version = reply_parsed[2]
    print(
        "METHOD: "
        + method
        + " RESOURCE: "
        + resource
        + " HTTP VERSION: "
        + http_version
        + "\n"
    )
    try:
        verify_method(
            method,
            cfg
        )  # Thows ValueError(405) if unsupported method, throws ValueError(400) if unknown
        check_if_forbidden(
            resource
        )  # Throws ValueError(403) if resorce path is outside of web_directory
        verify_http_version(
            http_version
        )  # Throws ValueError(505) if unsupported HTTP version
        if resource != "/":
            print(web_directory + resource)
        else:
            resource = "/index.html"

        with open(web_directory + resource, "rb") as file:
            file_contents = file.read()  # Throws IOError if file doesn't exist
        extension = get_file_type(resource, cfg)
        conn.send(http_version.encode() + b" 200 OK\r\n")
        conn.send(b"Content-Type: " + extension.encode() + b"\r\n")
        conn.send(b"\r\n")
        conn.send(file_contents)
        file.close()
    except IOError:
        conn.send(http_version.encode() + b" 404 Not Found\r\n")
        conn.send(b"Sorry we don't have that file!")
    except ValueError as error:
        errorCode = int(str(error))
        if errorCode == 403:
            conn.send(http_version.encode() + b" 403 Forbidden\r\n")
            conn.send(resource.encode() + b" is forbidden!")
        elif errorCode == 400:
            conn.send(http_version.encode() + b" 400 Bad Request\r\n")
            conn.send(method.encode() + b" is not a valid method!")
            print(400)
        elif errorCode == 405:
            conn.send(http_version.encode() + b" 405 Method Not Allowed\r\n")
            conn.send(method.encode() + b" is not supported by this server!")
            print(405)
        elif errorCode == 505:
            conn.send(http_version.encode() + b" 505 HTTP Version Not Supported\r\n")
            conn.send(
                http_version.encode() + b" is not a valid HTTP version! Try HTTP/1.1"
            )
    conn.close()
    print("Client Disconnected")
