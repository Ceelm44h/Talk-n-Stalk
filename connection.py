import socket
import threading

import net_utils
from stoppable_thread import StoppableThread

class Connection():
    """Connect two clients and exchange messages between them."""
    def __init__(self, conn_one, conn_two):
        self.conn_one = conn_one
        self.conn_two = conn_two

        net_utils.send(conn_two, net_utils.receive(conn_one))  # Exchange nicknames.
        net_utils.send(conn_one, net_utils.receive(conn_two))

        self.first_to_second = StoppableThread(target=self.repeater, args=(conn_one, conn_two))
        self.second_to_first = StoppableThread(target=self.repeater, args=(conn_two, conn_one))

    def run(self):
        """Start the connection."""
        self.is_open = True
        self.first_to_second.start()
        self.second_to_first.start()
   
    def repeater(self, sender, receiver):
        """Pass messages from sender to receiver."""    
        while not threading.current_thread().stopped() and self.is_open:
            try:
                msg = net_utils.receive(sender)
            except ConnectionResetError:
                msg = None
                self.close_connection(sender)
                
            if msg == net_utils.DISCONNECT_MSG:
                self.close_connection(sender)
            if msg:
                net_utils.send(receiver, msg)
    
    def close_connection(self, disconnecting_client):
        """Send disconnect messages and stop repeater threads."""
        if self.is_open:
            self.is_open = False
            print(f'Closing connection between {self.conn_one} and {self.conn_two}')
            if self.conn_one == disconnecting_client:
                net_utils.send(self.conn_two,  net_utils.DISCONNECT_MSG)
            elif self.conn_two == disconnecting_client:
                net_utils.send(self.conn_one, net_utils.DISCONNECT_MSG)
            else:
                net_utils.send(self.conn_one, net_utils.DISCONNECT_MSG)
                net_utils.send(self.conn_two,  net_utils.DISCONNECT_MSG)

            self.first_to_second.stop()
            self.second_to_first.stop()

    def __del__(self):
        self.close_connection(None)
