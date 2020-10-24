# includes
import socket
import threading
from server_functions import *

## MAIN FUNCTION ##
if __name__ == "__main__":
    # Read Configuration from config.txt
    cfg = read_config()
    host = cfg[0]
    port = cfg[1]
    web_directory = cfg[2]

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
