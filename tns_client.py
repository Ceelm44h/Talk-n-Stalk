import socket
import threading
import sys

from stoppable_thread import StoppableThread
import net_utils

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4205

class Client:
    def __del__(self):
        net_utils.send(self.server, net_utils.DISCONNECT_MSG)
        self.close_connection()

    def receiver(self, target, nick):
        """Receive all incoming messages from server while thread is active"""
        while not threading.current_thread().stopped():
            try:
                msg = net_utils.receive(target)
            except socket.error:
                msg = None
                self.close_connection()

            if msg == net_utils.DISCONNECT_MSG:
                print(f'User {self.interlocutor_nick} disconnected.')
                self.close_connection()
                break
            elif msg:
                print(nick + ": " + msg)

    def talker(self, server):
        """Send all given messages while thread is active"""
        while not threading.current_thread().stopped():
            msg = input()
            
            if msg:
                net_utils.send(server, msg)

            if msg == net_utils.DISCONNECT_MSG:
                self.close_connection()

    def close_connection(self):
        """"Stop active threads and close the connection."""
        if self.is_open:
            self.is_open = False
            self.talker_thr.stop()
            self.stalker_thr.stop()

            print('Disconnected.')
        
    def open_connection(self, server):
        """Start threads responsible for communication with server/"""
        if not self.is_open:
            self.is_open = True
            self.talker_thr = StoppableThread(target=self.talker, args=(server, ))
            self.stalker_thr = StoppableThread(target=self.receiver, args=(server, self.interlocutor_nick))

            self.talker_thr.start()
            self.stalker_thr.start()

    def start(self, args):
        self.nick = args[0]
        self.password = args[1]
        self.is_open = False

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        server.connect((SERVER, PORT))

        net_utils.send(server, self.nick)
        net_utils.send(server, self.password)
        #net_utils.send(server, self.password)
        net_utils.send(server, self.nick)  # Send own nickname.
        self.interlocutor_nick = net_utils.receive(server)  # Get interlocutor's nickname.
        
        self.open_connection(server)

        try:
            while self.is_open:
                pass
        except KeyboardInterrupt:
            net_utils.send(server, net_utils.DISCONNECT_MSG)
            self.close_connection()

def main(argv):
    client = Client()
    client.start(argv[1:])

if __name__ == '__main__':
    main(sys.argv)