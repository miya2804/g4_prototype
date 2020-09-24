from orator import DatabaseManager
from models import Room, set_connection


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
