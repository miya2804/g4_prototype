import logging
import random
from concurrent import futures

import grpc

from services import sensor_manager_pb2, sensor_manager_pb2_grpc

import mysql.connector as db
import configparser

N_DUMMY_SENSORS = 2
DUMMY_ROOM_ID = 1
DUMMY_HOST = '127.0.0.1:8080'
DUMMY_SUCCESS = True

logger = logging.getLogger(__name__)

class SensorManagerServicer(sensor_manager_pb2_grpc.SensorManagerServicer):
    def __init__(self, *args, **kwargs):
        super(SensorManagerServicer, self).__init__(*args, **kwargs)

    def Register(self, request, context):
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            cnx = db.connect(
                host=config.get('sensor-db', 'host'),
                port=config.getint('sensor-db', 'port'),
                user=config.get('sensor-db', 'user'),
                password=config.get('sensor-db', 'password'),
                database=config.get('sensor-db', 'database')
            )
            cur = cnx.cursor()
            cur.execute('insert into sensors values (null, %s, %s)',
                        (request.room_id, request.host))
            id = cur.lastrowid
            cnx.commit()
        except db.Error as e:
            logger.debug('DB error.', exc_info=True)
            success = False
        else:
            cur.close()
            cnx.close()
            success = True

        if success:
            sensors = [sensor_manager_pb2.Sensor(room_id=id,
                                                 host=request.host)]
        else:
            sensors = [sensor_manager_pb2.Sensor(room_id=None,
                                                 host=request.host)]
        return sensor_manager_pb2.Result(sensors=sensors,
                                         success=success)

    def Get(self, request, context):
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            cnx = db.connect(
                host=config.get('sensor-db', 'host'),
                port=config.getint('sensor-db', 'port'),
                user=config.get('sensor-db', 'user'),
                password=config.get('sensor-db', 'password'),
                database=config.get('sensor-db', 'database')
            )
            cur = cnx.cursor()
            cur.execute('select room_id,host from sensors where room_id= %s',
                        (request.room_id, ))
            db_res = cur.fetchall()
        except db.Error:
            logger.debug('DB error.', exc_info=True)
            success = False
        else:
            cur.close()
            cnx.close()
            success = True

        if success:
            sensors = []
            for row in db_res:
                sensors.append(sensor_manager_pb2.Sensor(room_id=row[0],
                                                         host=row[1]))
        else:
            sensors = [sensor_manager_pb2.Sensor(room_id=None,
                                                 host=None)]
        logger.info(sensors)
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
    logging.basicConfig(level=logging.DEBUG)
    serve()
