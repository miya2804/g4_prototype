import configparser

from orator import DatabaseManager
from models import Room, set_connection

CONFIG_NAME = 'mysql'
MYSQL_DRIVER_NAME = 'mysql'
CONFIG_SECTION = 'room-db'

class Manager():
    def __init__(self, db_config):
        db = DatabaseManager(db_config)
        set_connection(db)

    def register(self, password):
        room = Room()
        room.password = password
        try:
            room.save()
        except:
            return None, False
        return room.id, True

    def signin(self, id_, password):
        room = Room\
            .where('id', '=', id_)\
            .where('password', '=', password)\
            .get()

        if len(room) == 1:
            return True
        return False

    @classmethod
    def from_file(cls, path):
        config = configparser.ConfigParser()
        config.read(path)
        
        db_config = {
            CONFIG_NAME: {
                'driver': MYSQL_DRIVER_NAME,
                'host': config.get(CONFIG_SECTION, 'host'),
                'database': config.get(CONFIG_SECTION, 'database'),
                'user': config.get(CONFIG_SECTION, 'user'),
                'password': config.get(CONFIG_SECTION, 'password'),
                'prefix': '',
            }
        }
        
        return cls(db_config)
