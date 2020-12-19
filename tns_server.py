#!/usr/bin/env python3
import socket
import sys
import threading

import net_utils
import sqlbase
from stoppable_thread import StoppableThread
from connection import Connection

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4205

class Server():
    def __init__(self):
        self.sql = sqlbase.SQLBase()

    def __del__(self):
        for conn in self.activeConnections:
            conn.close_connection(None)

    def verify(self, conn, login, password):
        """Check if password is correct for given login."""
        id = self.sql.getUser(login, password)

        if id is None:
            print('Authorization failed.')
            net_utils.send(conn, 'Authorization failed.')
            return False
        
        net_utils.send(conn, 'Authorization succeeded.')
        print(f'User {login} connected.')
        return True

    def establish_connection(self, conn, connTwo):
        """Make connection between two clients."""
        print('Connection established.')
        connection = Connection(conn, connTwo)
        connection.run()
        
        self.activeConnections.append(connection)
    
                
    def run(self, args):
        """Run server on ip = SERVER and port = PORT"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((SERVER, PORT))
        server.listen()
        print('listening on', (SERVER, PORT))
        client_nr = 0
        self.activeConnections = list()

        try:
            while True:
                if client_nr % 2:
                    conn_second = server.accept()[0]
                    
                    sentNick = net_utils.receive(conn_second)
                    sentPass = net_utils.receive(conn_second)
   
                    if not self.verify(conn_second, sentNick, sentPass):
                        continue

                    client_nr += 1
                    self.establish_connection(conn_first, conn_second)
                else:
                    conn_first = server.accept()[0]

                    sentNick = net_utils.receive(conn_first)
                    sentPass = net_utils.receive(conn_first)
   
                    if not self.verify(conn_first, sentNick, sentPass):
                        continue

                    client_nr += 1

                print(f'{client_nr}. client connected')
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    serv = Server()
    serv.run(sys.argv)