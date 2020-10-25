# includes
import socket
import threading
from server_functions import *
from configparser import ConfigParser

## MAIN FUNCTION ##
if __name__ == "__main__":
    # Read Configuration from config.ini
    cfg = ConfigParser()
    cfg.read('config.ini')
    host = cfg.get('server', 'host')
    port = cfg.get('server', 'port')
    web_directory = cfg.get('server', 'web_directory')

    # This block of code handles the new clients and passes control to for_each_client()
    sock = socket.create_server((host, int(port)))
    print("Creating Server on " + host + ":" + port + "\r\n")
    while True:
        sock.listen(10)
        conn = sock.accept()[0]
        print("Client Connected")
        new_thread = threading.Thread(
            None, for_each_client, None, (sock, conn, web_directory)
        )
        new_thread.start()
