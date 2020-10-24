# This function gets the correct file type, and returns the Content-Type to be sent to the client
def get_file_type(file):
    ret = "text"
    extension = file.split(".")[1]
    if extension == "html":
        ret = "text/html; charset=UTF-8"
    elif extension == "ico":
        ret = "image/x-icon"
    elif extension == "css":
        ret = "text/css; charset=UTF-8"
    elif extension == "jpg":
        ret = "image/jpeg"
    elif extension == "pdf":
        ret = "application/pdf"
    else:
        ret = "text; charset=UTF-8"

    return ret


# This function makes sure the request stays in the bounds of the web directory
def check_if_forbidden(file):
    updir = file.count("..") + 1
    downdir = file.count("/") + 1
    if updir == 0 or downdir / updir < 2:
        raise ValueError(403)


def verify_method(method):
    valid = {
        "GET": True,
        "HEAD": False,
        "POST": False,
        "PUT": False,
        "DELETE": False,
        "CONNECT": False,
        "OPTIONS": False,
        "TRACE": False,
    }
    if (method in valid) == False:
        raise ValueError(400)
    elif valid[method] == False:
        raise ValueError(405)


def verify_http_version(http_version):
    if http_version != "HTTP/1.1":
        raise ValueError(505)


# This function will be run for every client that connects
def for_each_client(sock, conn, web_directory):
    reply_raw = str(conn.recv(4096))[2:-1]
    if reply_raw == "":  # checks if client disconnected without sending request
        print("Client Disconnected")
        return None
    requests = reply_raw.split("\\r\\n")
    reply_parsed = requests[0].split(" ")
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
        verify_method(method)  # Thows ValueError(405) if unsupported method, throws ValueError(400) if unknown
        check_if_forbidden(resource)  # Throws ValueError(403) if resorce path is outside of web_directory
        verify_http_version(http_version)  # Throws ValueError(505) if unsupported HTTP version
        if resource != "/":
            print(web_directory + resource)
        else:
            resource = "/index.html"

        file = open(web_directory + resource, "rb")  # Throws IOError if file doesn't exist
        extension = get_file_type(resource)
        conn.send(http_version.encode() + b" 200 OK\r\n")
        conn.send(b"Content-Type: " + extension.encode() + b"\r\n")
        conn.send(b"\r\n")
        conn.send(file.read())
        file.close()
    except IOError:
        conn.send(http_version.encode() + b" 404 Not Found")
        conn.send(b"\r\n")
        conn.send(b"Sorry we don't have that file!")
    except ValueError as error:
        errorCode = int(str(error))
        if errorCode == 403:
            conn.send(http_version.encode() + b" 403 Forbidden")
            conn.send(b"\r\n")
            conn.send(resource.encode() + b" is forbidden!")
        elif errorCode == 400:
            conn.send(http_version.encode() + b" 400 Bad Request")
            conn.send(b"\r\n")
            conn.send(method.encode() + b" is not a valid method!")
        elif errorCode == 405:
            conn.send(http_version.encode() + b" 405 Method Not Allowed")
            conn.send(b"\r\n")
            conn.send(method.encode() + b" is not supported by this server!")
        elif errorCode == 505:
            conn.send(http_version.encode() + b" 505 HTTP Version Not Supported")
            conn.send(b"\r\n")
            conn.send(http_version.encode() + b" is not a valid HTTP version! Try HTTP/1.1")
    conn.close()
    print("Client Disconnected")


# This function parses the config file for use in the program. Returns (host, port, web directory)
def read_config():
    cfgFile = open("config.txt", "r")
    cfg = cfgFile.read()
    cfg_parsed = cfg.split("\n")
    return (
        cfg_parsed[0].split(" ")[1],
        cfg_parsed[1].split(" ")[1],
        cfg_parsed[2].split(" ")[1],
    )
