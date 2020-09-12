import json

import grpc
from flask import Flask, request, jsonify, Response

from services import rasp_pb2, rasp_pb2_grpc
from services import room_manager_pb2, room_manager_pb2_grpc
from services import sensor_manager_pb2, sensor_manager_pb2_grpc

DUMMY_ROOM_ID=1
DUMMY_PASSWORD='password'
DUMMY_RASP1_ID=1
DUMMY_RASP2_ID=2
DUMMY_HOST='127.0.0.1:8080'
DEFAULT_PORT = 50051
TIMEOUT = 5

app = Flask(__name__)

@app.route('/room/<room_id>', methods=['GET'])
def get_states(room_id):
    password = request.args.get('password')
    if password is None:
        return Response(response='Bad Request', status=400)

    with grpc.insecure_channel('room:50051') as channel:
        stub = room_manager_pb2_grpc.RoomManagerStub(channel)
        room = room_manager_pb2.Room(id=int(room_id),
                                     password=password)
        result = stub.Signin(room)

    if not result.success:
        return Response(response='Bad Request', status=400)

    with grpc.insecure_channel('sensor:50051') as channel:
        stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
        sensor = sensor_manager_pb2.Sensor(room_id=DUMMY_ROOM_ID)
        result = stub.Get(sensor)

    if not result.success:
        return Response(response='Internal Server Error', status=500)

    resp = {}
    # FIX センサーのデータにIDが存在しないため,一旦インデックスで代用
    # messageが修正されたらIDに修正

    for idx, sensor in enumerate(result.sensors):
        addr = '{}:{}'.format(sensor.host, DEFAULT_PORT)
        with grpc.insecure_channel(addr) as channel:
            stub = rasp_pb2_grpc.RaspStub(channel)
            empty = rasp_pb2.Empty()
            try:
                state = stub.GetState(empty, timeout=TIMEOUT)
                resp[idx] = {'state': {'opened': state.opened}}
            except:
                resp[idx] = {'state': {'opened': None}}

    return Response(response=json.dumps(resp), status=200)

@app.route('/room', methods=['POST'])
def register_room():
    payload = request.json
    password = payload.get('password')
    if password is None:
        return Response(response='Bad Request', status=400)

    with grpc.insecure_channel('room:50051') as channel:
        stub = room_manager_pb2_grpc.RoomManagerStub(channel)
        room = room_manager_pb2.Room(password=password)
        result = stub.Register(room)

    if not result.success:
        return Response(response='Internal Server Error', status=500)

    resp = {'id': result.id, 'success': result.success}

    return Response(response=json.dumps(resp), status=200)

@app.route('/sensor', methods=['POST'])
def register_sensor():
    payload = request.json
    room_id = payload.get('room_id')
    host = payload.get('host')
    if room_id is None or host is None:
        return Response(response='Bad Request', status=400)

    with grpc.insecure_channel('sensor:50051') as channel:
        stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
        sensor = sensor_manager_pb2.Sensor(room_id=room_id,
                                           host=host)
        result = stub.Register(sensor)

    if not result.success:
        return Response(response='Internal Server Error', status=500)

    resp = {'id': result.sensors[0].room_id, 'success': result.success}

    return Response(response=json.dumps(resp), status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
