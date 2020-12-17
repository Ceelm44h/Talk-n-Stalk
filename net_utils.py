import socket

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = ":disconnect:"

def send(target, msg):
    """Send a message with padding to the target"""
    msg = msg.encode(FORMAT)
    msgLength = len(msg)
    msgLength = str(msgLength).encode(FORMAT)
    msgLength += b' ' * (HEADER - len(msgLength))

    target.send(msgLength)
    target.send(msg)

def receive(target):
    msgLength = target.recv(HEADER).decode(FORMAT)
        
    if msgLength:
        msgLength = int(msgLength)
        msg = target.recv(msgLength).decode(FORMAT)
        return msg