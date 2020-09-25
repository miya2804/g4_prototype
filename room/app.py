import random
import logging
from concurrent import futures

import grpc
from orator import DatabaseManager

from services import room_manager_pb2, room_manager_pb2_grpc

from manager import Manager


DB_CONFIG_PATH = './config.ini'
manager = Manager.from_file(DB_CONFIG_PATH)

class RoomManagerServicer(room_manager_pb2_grpc.RoomManagerServicer):
    def __init__(self, *args, **kwargs):
        super(RoomManagerServicer, self).__init__(*args, **kwargs)

    def Register(self, request, context):
        id_, success = manager.register(request.password)
        return room_manager_pb2.Result(id=id_,
                                       success=success)

    def Signin(self, request, context):
        id_ = request.id
        success = manager.signin(id_, request.password)
        return room_manager_pb2.Result(id=id_,
                                       success=success)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    room_manager_pb2_grpc.\
        add_RoomManagerServicer_to_server(RoomManagerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
