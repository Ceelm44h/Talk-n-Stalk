#!/usr/bin/env python3
import socket
import sys
import threading

import net_utils
from stoppable_thread import StoppableThread
from connection import Connection

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4205

def establish_connection(conn, addr, connTwo, addrTwo):
    connection = Connection(conn, connTwo)
    connection.run()
        
def main(args):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print('listening on', (SERVER, PORT))
    client_nr = 0

    try:
        while True:
            if client_nr % 2:
                conn_second, addr_second = server.accept()
                client_nr += 1
                establish_connection(conn_first, addr_first, conn_second, addr_second)
            else:
                conn_first, addr_first = server.accept()
                client_nr += 1

            print(f'{client_nr}. client connected')
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main(sys.argv)