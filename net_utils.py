import socket

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = ':disconnect:'

def send(target, msg):
    """Send a message with padding to the target"""
    msg = msg.encode(FORMAT)
    msg_length = len(msg)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))

    target.send(msg_length)
    target.send(msg)

def receive(target):
    msg_length = target.recv(HEADER).decode(FORMAT)
        
    if msg_length:
        msg_length = int(msg_length)
        msg = target.recv(msg_length).decode(FORMAT)
        return msg