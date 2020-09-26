import logging
from concurrent import futures

import grpc

import dbmanager
from services import sensor_manager_pb2, sensor_manager_pb2_grpc

CONFIG_PATH = 'config.ini'
SECTION = 'sensor-db'

logger = logging.getLogger(__name__)


class SensorManagerServicer(sensor_manager_pb2_grpc.SensorManagerServicer):
    def __init__(self, *args, **kwargs):
        super(SensorManagerServicer, self).__init__(*args, **kwargs)

    def Register(self, request, context):
        db = dbmanager.SensordbManager(CONFIG_PATH, SECTION)
        id_, success = db.register_sensor(request.room_id, request.host)

        sensors = []
        if success:
            sensors = [sensor_manager_pb2.Sensor(room_id=id_)]

        return sensor_manager_pb2.Result(sensors=sensors,
                                         success=success)

    def Get(self, request, context):
        db = dbmanager.SensordbManager(CONFIG_PATH, SECTION)
        sensor_list, success = db.get_sensors(request.room_id)

        sensors = []
        if success:
            for sensor in sensor_list:
                sensors.append(sensor_manager_pb2.Sensor
                               (id=sensor[0],
                                room_id=sensor[1],
                                host=sensor[2]))

        return sensor_manager_pb2.Result(sensors=sensors,
                                         success=success)


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
