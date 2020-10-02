import json
import configparser
from http import HTTPStatus

from flask import Flask, Response, request, jsonify, send_from_directory


from services import rasp_pb2, rasp_pb2_grpc
from services import room_manager_pb2, room_manager_pb2_grpc
from services import sensor_manager_pb2, sensor_manager_pb2_grpc

from clients import RoomClient, SensorClient, RaspClient

CONFIG_PATH = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

app = Flask(__name__, static_folder='./public')

room_addr = '{}:{}'.format(config.get('room', 'Host'),
                           config.get('room', 'Port'))
sensor_addr = '{}:{}'.format(config.get('sensor', 'Host'),
                             config.get('sensor', 'Port'))
room_client = RoomClient(room_addr,
                         timeout=config.getint('room', 'Timeout'))
sensor_client = SensorClient(sensor_addr,
                             timeout=config.getint('sensor', 'Timeout'))

@app.route('/api/room/<room_id>', methods=['GET'])
def get_states(room_id):
    password = request.args.get('password')
    if password is None:
        return Response(response='Bad Request',
                        status=HTTPStatus.BAD_REQUEST)

    success = room_client.signin(int(room_id), password)
    if not success:
        return Response(response='Bad Request',
                        status=HTTPStatus.BAD_REQUEST)

    sensors, success = sensor_client.get(int(room_id))
    if not success:
        return Response(response='Internal Server Error',
                        status=HTTPStatus.INTERNAL_SERVER_ERROR)

    resp = {}
    for sensor in sensors:
        addr = '{}:{}'.format(sensor.host, config.get('sensor', 'Port'))
        opened = RaspClient.get_state_with_address(addr,
                                                   timeout=config.getint('sensor', 'Timeout'))
        resp[sensor.id] = {'state': {'opened': opened}}

    return Response(response=json.dumps(resp),
                    status=HTTPStatus.OK)

@app.route('/api/room', methods=['POST'])
def register_room():
    payload = request.json
    password = payload.get('password')
    if password is None:
        return Response(response='Bad Request',
                        status=HTTPStatus.BAD_REQUEST)

    id_, success = room_client.register(password)
    if not success:
        return Response(response='Internal Server Error',
                        status=HTTPStatus.INTERNAL_SERVER_ERROR)

    resp = {'id': id_, 'success': success}

    return Response(response=json.dumps(resp),
                    status=HTTPStatus.OK)

@app.route('/api/sensor', methods=['POST'])
def register_sensor():
    payload = request.json
    room_id = payload.get('room_id')
    password = payload.get('password')
    host = payload.get('host')
    if any(list(map(lambda x: x is None, [room_id, password, host]))):
        return Response(response='Bad Request',
                        status=HTTPStatus.BAD_REQUEST)

    success = room_client.signin(int(room_id), password)
    if not success:
        return Response(response='Bad Request',
                        status=HTTPStatus.BAD_REQUEST)

    id_, success = sensor_client.register(room_id, host)
    if not success:
        return Response(response='Internal Server Error',
                        status=HTTPStatus.INTERNAL_SERVER_ERROR)

    resp = {'id': id_, 'success': success}

    return Response(response=json.dumps(resp),
                    status=HTTPStatus.OK)

@app.route('/', methods=['GET'])
def root():
    return send_from_directory('public', 'index.html')

if __name__ == '__main__':
    app.run(host=config.get('master', 'Host'),
            port=config.getint('master', 'Port'))
