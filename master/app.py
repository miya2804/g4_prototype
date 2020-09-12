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

app = Flask(__name__)

@app.route('/room', methods=['GET'])
def get_states():
    with grpc.insecure_channel('room:50051') as channel:
        stub = room_manager_pb2_grpc.RoomManagerStub(channel)
        room = room_manager_pb2.Room(id=DUMMY_ROOM_ID,
                                     password=DUMMY_PASSWORD)
        _ = stub.Signin(room)

    with grpc.insecure_channel('sensor:50051') as channel:
        stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
        sensor = sensor_manager_pb2.Sensor(room_id=DUMMY_ROOM_ID)
        _ = stub.Get(sensor)

    resp = {}
    with grpc.insecure_channel('rasp1:50051') as channel:
        stub = rasp_pb2_grpc.RaspStub(channel)
        empty = rasp_pb2.Empty()
        state = stub.GetState(empty)
        resp[DUMMY_RASP1_ID] = {'state': {'opened': state.opened}}

    with grpc.insecure_channel('rasp2:50051') as channel:
        stub = rasp_pb2_grpc.RaspStub(channel)
        empty = rasp_pb2.Empty()
        state = stub.GetState(empty)
        resp[DUMMY_RASP2_ID] = {'state': {'opened': state.opened}}

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
    with grpc.insecure_channel('sensor:50051') as channel:
        stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
        sensor = sensor_manager_pb2.Sensor(room_id=DUMMY_ROOM_ID,
                                           host=DUMMY_HOST)
        result = stub.Register(sensor)

    resp = {'id': result.sensors[0].room_id, 'success': result.success}

    return Response(response=json.dumps(resp), status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
