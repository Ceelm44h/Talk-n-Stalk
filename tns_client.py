import socket
import threading
import sys

import net_utils

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 4202

def receiver(target, nick):
    while True:
        msg = net_utils.receive(target)

        if msg == net_utils.DISCONNECT_MSG:
            print("disconnected")
            break
        elif msg != None:
            print(nick + ": " + msg)

def talker(server):
    while True:
        msg = input()
        #if msg == net_utils.DISCONNECT_MSG:
        #    net_utils.send(server, net_utils.DISCONNECT_MSG)
        #    break
        if msg:
            net_utils.send(server, msg)

def main(args):
    nick = args[1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVER, PORT))

    net_utils.send(server, nick)
    interlocutor = net_utils.receive(server)

    talkerThr = threading.Thread(target=talker, args=(server, ))
    stalkerThr = threading.Thread(target=receiver, args=(server, interlocutor))

    talkerThr.start()
    stalkerThr.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        net_utils.send(server, net_utils.DISCONNECT_MSG)

if __name__ == "__main__":
    main(sys.argv)