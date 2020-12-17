import socket
import threading
import sys

from stoppable_thread import StoppableThread
import net_utils

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4202

class Client:
    def receiver(self, target, nick):
        """Receive all incoming messages from server while thread is active"""
        while not threading.current_thread().stopped():
            msg = net_utils.receive(target)

            if msg == net_utils.DISCONNECT_MSG:
                self.close()
                break
            elif msg != None:
                print(nick + ": " + msg)

    def talker(self, server):
        """Send all given messages while thread is active"""
        while not threading.current_thread().stopped():
            msg = input()
            if msg == net_utils.DISCONNECT_MSG:
                #self.close()
                #net_utils.send(server, net_utils.DISCONNECT_MSG)
                break
            if msg:
                net_utils.send(server, msg)

    def close(self):
        self.talkerThr.stop()
        self.stalkerThr.stop()
        print("Disconnected.")

    def start(self, nick):
        self.nick = nick
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((SERVER, PORT))

        net_utils.send(server, nick)  # Send own nickname.
        interlocutorNick = net_utils.receive(server)  # Get interlocutor's nickname.

        self.talkerThr = StoppableThread(target=self.talker, args=(server, ))
        self.stalkerThr = StoppableThread(target=self.receiver, args=(server, interlocutorNick))

        self.talkerThr.start()
        self.stalkerThr.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            net_utils.send(server, net_utils.DISCONNECT_MSG)
            self.close()

def main(argv):
    client = Client()
    client.start(argv[1])

if __name__ == "__main__":
    main(sys.argv)