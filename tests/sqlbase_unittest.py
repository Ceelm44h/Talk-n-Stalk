import unittest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import sqlbase

class SQLBaseTest(unittest.TestCase):
    def test_get_user_if_exists(self):
        sql = sqlbase.SQLBase()
        res = sql.get_user('admin', 'admin')
        self.assertEqual(res, True)

    def test_get_user_if_not_exists(self):
        sql = sqlbase.SQLBase()
        res = sql.get_user('zuberek', 'zuberek')
        self.assertEqual(res, False)

    def test_get_user_wrong_password(self):
        sql = sqlbase.SQLBase()
        res = sql.get_user('admin', 'user')
        self.assertEqual(res, False)

    def test_add_user_if_in_base(self):
        sql = sqlbase.SQLBase()
        res = sql.get_user('admin', 'admin')
        self.assertEqual(res, True)

    def test_add_user_if_not_in_base(self):
        sql = sqlbase.SQLBase()
        res = sql.get_user('zubr', 'zubr')
        self.assertEqual(res, False)

    def test_remove_user_if_in_base(self):
        sql = sqlbase.SQLBase()
        res = sql.remove_user('admin', 'admin')
        self.assertEqual(res, True)

    def test_remove_user_if_not_in_base(self):
        sql = sqlbase.SQLBase()
        res = sql.remove_user('zubrr', 'zubrr')
        self.assertEqual(res, False)

if __name__ == '__main__':
    unittest.main()