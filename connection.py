import socket
import threading

import net_utils
from stoppable_thread import StoppableThread

class Connection():
    """Connect two clients and exchange messages between them."""
    def __init__(self, connOne, connTwo):
        self.connOne = connOne
        self.connTwo = connTwo

        net_utils.send(connTwo, net_utils.receive(connOne))  # Exchange nicknames.
        net_utils.send(connOne, net_utils.receive(connTwo))

        self.firstToSecond = StoppableThread(target=self.repeater, args=(connOne, connTwo))
        self.secondToFirst = StoppableThread(target=self.repeater, args=(connTwo, connOne))

    def run(self):
        """Start the connection."""
        self.firstToSecond.start()
        self.secondToFirst.start()
   
    def repeater(self, sender, receiver):
        """Pass messages from sender to receiver."""    
        while not threading.current_thread().stopped():
            msg = net_utils.receive(sender)
            if msg == net_utils.DISCONNECT_MSG:
                self.close()
            if msg:
                net_utils.send(receiver, msg)
    
    def close(self):
        """Send disconnect messages and stop repeater threads."""
        net_utils.send(self.connOne, net_utils.DISCONNECT_MSG)
        net_utils.send(self.connTwo, net_utils.DISCONNECT_MSG)
        self.firstToSecond.stop()
        self.secondToFirst.stop()

    def __del__(self):
        self.close()