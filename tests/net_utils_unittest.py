import unittest
import socket
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import net_utils

class NetUtilsTest(unittest.TestCase):
    def test_send_target_exists(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((socket.gethostbyname(socket.gethostname()), 4205))   # Otwarty
        res = net_utils.send(server, 'test')
        self.assertEqual(res, True)

    def test_send_target_not_exists(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((socket.gethostbyname(socket.gethostname()), 4202))   # Zamknięty
        res = net_utils.send(server, 'test')
        self.assertEqual(res, False)

if __name__ == '__main__':
    unittest.main()