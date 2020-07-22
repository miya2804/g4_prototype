import json

import grpc
from flask import Flask, request, jsonify

from services import rasp_pb2, rasp_pb2_grpc
from services import room_manager_pb2, room_manager_pb2_grpc
from services import sensor_manager_pb2, sensor_manager_pb2_grpc

DUMMY_ROOM_ID=1
DUMMY_PASSWORD='password'
DUMMY_RASP1_ID=1
DUMMY_RASP2_ID=2
DUMMY_HOST='127.0.0.1:8080'

app = Flask(__name__)

@app.route('/', methods=['GET'])
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

    return jsonify(resp)

@app.route('/room', methods=['POST'])
def register_room():
    with grpc.insecure_channel('room:50051') as channel:
        stub = room_manager_pb2_grpc.RoomManagerStub(channel)
        room = room_manager_pb2.Room(password=DUMMY_PASSWORD)
        result = stub.Register(room)

    resp = {'id': result.id, 'success': result.success}
    return jsonify(resp)

@app.route('/sensor', methods=['POST'])
def register_sensor():
    with grpc.insecure_channel('sensor:50051') as channel:
        stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
        sensor = sensor_manager_pb2.Sensor(room_id=DUMMY_ROOM_ID,
                                           host=DUMMY_HOST)
        result = stub.Register(sensor)

    resp = {'id': result.sensors[0].room_id, 'success': result.success}
    return jsonify(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
