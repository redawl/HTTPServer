#includes
import socket
import threading
from server_functions import *

#This function parses the config file for use in the program. Returns (host, port, web directory)
def read_config():
	cfgFile = open("config.txt", "r")
	cfg = cfgFile.read()
	cfg_parsed = cfg.split("\n")
	return (cfg_parsed[0].split(" ")[1], cfg_parsed[1].split(" ")[1], cfg_parsed[2].split(" ")[1])

## MAIN FUNCTION ##

#Read Configuration from config.txt
cfg = read_config()
host = cfg[0]
port = cfg[1]
web_directory = cfg[2]

#This block of code handles the new clients and passes control to for_each_client()
sock = socket.create_server((host, int(port)))
while(1):
	sock.listen(10)
	conn = sock.accept()[0]
	print('Client Connected')
	new_thread = threading.Thread(None, for_each_client, None, (sock, conn, web_directory))
	new_thread.start()
