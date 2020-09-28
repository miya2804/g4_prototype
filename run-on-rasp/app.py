import logging
from concurrent import futures
import random
import RPi.GPIO as GPIO

import grpc

from services import rasp_pb2, rasp_pb2_grpc

DEFAULT_OPENED_VALUE=True
RANDOM_OPENED=False
REEDSWITCH = 4

class RaspServicer(rasp_pb2_grpc.RaspServicer):
    def GetState(self, request, context):
        opened=DEFAULT_OPENED_VALUE
        if RANDOM_OPENED:
            opened = bool(random.randint(0, 1))
        else:
            if GPIO.input(REEDSWITCH):
                opened = False
            else:
                opened = True
        return rasp_pb2.State(opened=opened)


def serve():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(REEDSWITCH, GPIO.IN)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rasp_pb2_grpc.add_RaspServicer_to_server(RaspServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
