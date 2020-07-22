import logging
import random
from concurrent import futures

import grpc

from services import room_manager_pb2, room_manager_pb2_grpc


DUMMY_ID = 1
DUMMY_SUCCESS = True


class RoomManagerServicer(room_manager_pb2_grpc.RoomManagerServicer):
    def __init__(self, *args, **kwargs):
        super(RoomManagerServicer, self).__init__(*args, **kwargs)

    def Register(self, request, context):
        return room_manager_pb2.Result(id=DUMMY_ID,
                                       success=DUMMY_SUCCESS)

    def Signin(self, request, context):
        return room_manager_pb2.Result(id=DUMMY_ID,
                                       success=DUMMY_SUCCESS)

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
