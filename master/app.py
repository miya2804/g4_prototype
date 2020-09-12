import json

import grpc
from flask import Flask, request, jsonify, Response

from services import rasp_pb2, rasp_pb2_grpc
from services import room_manager_pb2, room_manager_pb2_grpc
from services import sensor_manager_pb2, sensor_manager_pb2_grpc

from clients import RoomClient, SensorClient, RaspClient

DEFAULT_PORT = 50051

app = Flask(__name__)

room_client = RoomClient('room:50051')
sensor_client = SensorClient('sensor:50051')

@app.route('/room/<room_id>', methods=['GET'])
def get_states(room_id):
    password = request.args.get('password')
    if password is None:
        return Response(response='Bad Request', status=400)

    success = room_client.signin(int(room_id), password)
    if not success:
        return Response(response='Bad Request', status=400)

    sensors, success = sensor_client.get(int(room_id))
    if not success:
        return Response(response='Internal Server Error', status=500)

    resp = {}
    # FIX センサーのデータにIDが存在しないため,一旦インデックスで代用
    # messageが修正されたらIDに修正
    for idx, sensor in enumerate(sensors):
        addr = '{}:{}'.format(sensor.host, DEFAULT_PORT)
        opened = RaspClient.get_state_with_address(addr)
        resp[idx] = {'state': {'opened': opened}}

    return Response(response=json.dumps(resp), status=200)

@app.route('/room', methods=['POST'])
def register_room():
    payload = request.json
    password = payload.get('password')
    if password is None:
        return Response(response='Bad Request', status=400)

    id_, success = room_client.register(password)
    if not success:
        return Response(response='Internal Server Error', status=500)

    resp = {'id': id_, 'success': success}

    return Response(response=json.dumps(resp), status=200)

@app.route('/sensor', methods=['POST'])
def register_sensor():
    payload = request.json
    room_id = payload.get('room_id')
    host = payload.get('host')
    if room_id is None or host is None:
        return Response(response='Bad Request', status=400)

    id_, success = sensor_client.register(room_id, host)
    if not success:
        return Response(response='Internal Server Error', status=500)

    resp = {'id': id_, 'success': success}

    return Response(response=json.dumps(resp), status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
