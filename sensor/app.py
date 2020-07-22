import logging
import random
from concurrent import futures

import grpc

from services import sensor_manager_pb2, sensor_manager_pb2_grpc

N_DUMMY_SENSORS = 2
DUMMY_ROOM_ID = 1
DUMMY_HOST = '127.0.0.1:8080'
DUMMY_SUCCESS = True

class SensorManagerServicer(sensor_manager_pb2_grpc.SensorManagerServicer):
    def __init__(self, *args, **kwargs):
        super(SensorManagerServicer, self).__init__(*args, **kwargs)

    def Register(self, request, context):
        sensors = [sensor_manager_pb2.Sensor(room_id=DUMMY_ROOM_ID,
                                             host=DUMMY_HOST)]
        return sensor_manager_pb2.Result(sensors=sensors,
                                         success=DUMMY_SUCCESS)

    def Get(self, request, context):
        sensors = [sensor_manager_pb2.Sensor(room_id=DUMMY_ROOM_ID,
                                             host=DUMMY_HOST)
                   for _ in range(N_DUMMY_SENSORS)]
        return sensor_manager_pb2.Result(sensors=sensors,
                                         success=DUMMY_SUCCESS)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_manager_pb2_grpc.\
        add_SensorManagerServicer_to_server(SensorManagerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
