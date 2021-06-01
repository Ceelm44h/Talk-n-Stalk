import unittest
import socket
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import tns_server

class ServerTest(unittest.TestCase):
    def test_verify_user_exists(self):
        server = tns_server.Server()
        res = server.checkCredentials('admin', 'admin')
        self.assertEqual(res, True)
    
    def test_verify_user_not_exists(self):
        server = tns_server.Server()
        res = server.checkCredentials('zubrewar', 'zureawreawreawbr')
        self.assertEqual(res, False)

if __name__ == '__main__':
    unittest.main()