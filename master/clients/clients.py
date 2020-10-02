import grpc
import requests

from services import rasp_pb2, rasp_pb2_grpc
from services import room_manager_pb2, room_manager_pb2_grpc
from services import sensor_manager_pb2, sensor_manager_pb2_grpc


class ClientBase():
    def __init__(self, addr, timeout=None, grpc=True):
        self.addr = addr
        self.timeout= timeout
        self.grpc = grpc


class RoomClient(ClientBase):
    def register(self, password):
        with grpc.insecure_channel(self.addr) as channel:
            stub = room_manager_pb2_grpc.RoomManagerStub(channel)
            room = room_manager_pb2.Room(password=password)
            result = stub.Register(room, timeout=self.timeout)
        
        return result.id, result.success

    def signin(self, id_, password):
        with grpc.insecure_channel(self.addr) as channel:
            stub = room_manager_pb2_grpc.RoomManagerStub(channel)
            room = room_manager_pb2.Room(id=id_,
                                         password=password)
            result = stub.Signin(room, timeout=self.timeout)
            
        return result.success


class SensorClient(ClientBase):
    def get(self, room_id):
        with grpc.insecure_channel(self.addr) as channel:
            stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
            sensor = sensor_manager_pb2.Sensor(room_id=room_id)
            result = stub.Get(sensor, timeout=self.timeout)

        return result.sensors, result.success

    def register(self, room_id, host):
        with grpc.insecure_channel(self.addr) as channel:
            stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
            sensor = sensor_manager_pb2.Sensor(room_id=room_id,
                                               host=host)
            result = stub.Register(sensor, timeout=self.timeout)

        if result.success:
            return result.sensors[0].room_id, result.success
        else:
            return None, result.success


class RaspClient(ClientBase):
    def get_state(self):
        if self.grpc:
            with grpc.insecure_channel(self.addr) as channel:
                stub = rasp_pb2_grpc.RaspStub(channel)
                empty = rasp_pb2.Empty()
                try:
                    state = stub.GetState(empty, timeout=self.timeout)
                except:
                    return None

            return state.opened

        else:
            try:
                return requests.get(self.addr).json()['opened']
            except:
                return None


    @classmethod
    def get_state_with_host_and_port(cls, host, port,
                                     timeout=None, grpc=True):
        if grpc:
            addr = '{}:{}'.format(host, port)

        else:
            addr = 'http://{}:{}'.format(host, 3000)

        client = cls(addr, timeout, grpc)
        return client.get_state()
