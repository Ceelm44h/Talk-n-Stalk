#!/usr/bin/env python3
import socket
import sys
import threading

import net_utils
from stoppable_thread import StoppableThread
from connection import Connection

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4202

def establishConnection(conn, addr, connTwo, addrTwo):
    connection = Connection(conn, connTwo)
    connection.run()
        
def main(args):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print("listening on", (SERVER, PORT))
    clientNr = 1
    
    while True:
        if clientNr % 2 == 0:
            connSecond, addrSecond = server.accept()
            clientNr += 1
            print(f"{clientNr} client connected")
            establishConnection(connFirst, addrFirst, connSecond, addrSecond)
        else:
            connFirst, addrFirst = server.accept()
            clientNr += 1

if __name__ == "__main__":
    main(sys.argv)