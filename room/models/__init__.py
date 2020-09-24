from .room import Room

def set_connection(db):
    from orator import Model
    Model.set_connection_resolver(db)
