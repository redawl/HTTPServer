# includes
import socket
import threading
from server_functions import *
from configparser import ConfigParser
from datetime import datetime

## MAIN FUNCTION ##
if __name__ == "__main__":
    # Read Configuration from config.ini
    cfg = ConfigParser()
    cfg.read("config.ini")
    host = cfg.get("server", "host")
    port = cfg.get("server", "port")
    web_directory = cfg.get("server", "web_directory")

    # This block of code handles the new clients and passes control to for_each_client()
    sock = socket.create_server((host, int(port)))
    print("Creating Server on " + host + ":" + port + "\r\n")
    while True:
        sock.listen(10)
        conn = sock.accept()[0]
        print("Client Connected [", datetime.now(), "]")
        if threading.active_count() <= 500:
            new_thread = threading.Thread(
                None, for_each_client, None, (sock, conn, web_directory, cfg)
            )
            new_thread.start()
        else:
            conn.send(b"HTTP/1.1 503 Service Unavailable\r\n")
            conn.send(b"Too many requests ATM. Please try again later!")
            conn.close()
            print("Client Disconnected")
