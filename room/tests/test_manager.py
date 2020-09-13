import unittest

from orator import DatabaseManager

from manager import Manager


DB_CONFIG = {
    'mysql': {
        'driver': 'mysql',
        'host': 'room-db',
        'database': 'test_rooms',
        'user': 'root',
        'password': 'password',
        'prefix': '',
    }
}


class TestManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestManager, self).__init__(*args, **kwargs)
        self.manager = Manager(DB_CONFIG)

    def setUp(self):
        db = DatabaseManager(DB_CONFIG)
        db.table('rooms').truncate()

    def test_register_at_first(self):
        password = 'test'
        id_, success = self.manager.register(password)

        self.assertEqual(id_, 1)
        self.assertTrue(success)

    def test_signin_empty_database(self):
        id_ = 1
        password = 'test'
        success = self.manager.signin(id_, password)

        self.assertFalse(success)

    def test_signin_after_register(self):
        password = 'test'
        id_, _ = self.manager.register(password)
        success = self.manager.signin(id_, password)

        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
