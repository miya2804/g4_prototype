import grpc

from services import rasp_pb2, rasp_pb2_grpc
from services import room_manager_pb2, room_manager_pb2_grpc
from services import sensor_manager_pb2, sensor_manager_pb2_grpc


TIMEOUT = 5


class ClientBase():
    def __init__(self, addr):
        self.addr = addr


class RoomClient(ClientBase):
    def register(self, password):
        with grpc.insecure_channel(self.addr) as channel:
            stub = room_manager_pb2_grpc.RoomManagerStub(channel)
            room = room_manager_pb2.Room(password=password)
            result = stub.Register(room)
        
        return result.id, result.success

    def signin(self, id_, password):
        with grpc.insecure_channel(self.addr) as channel:
            stub = room_manager_pb2_grpc.RoomManagerStub(channel)
            room = room_manager_pb2.Room(id=id_,
                                         password=password)
            result = stub.Signin(room)
            
        return result.success


class SensorClient(ClientBase):
    def get(self, room_id):
        with grpc.insecure_channel(self.addr) as channel:
            stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
            sensor = sensor_manager_pb2.Sensor(room_id=room_id)
            result = stub.Get(sensor)

        return result.sensors, result.success

    def register(self, room_id, host):
        with grpc.insecure_channel(self.addr) as channel:
            stub = sensor_manager_pb2_grpc.SensorManagerStub(channel)
            sensor = sensor_manager_pb2.Sensor(room_id=room_id,
                                               host=host)
            result = stub.Register(sensor)

        return result.sensors[0].room_id, result.success


class RaspClient(ClientBase):
    def get_state(self):
        with grpc.insecure_channel(self.addr) as channel:
            stub = rasp_pb2_grpc.RaspStub(channel)
            empty = rasp_pb2.Empty()
            try:
                state = stub.GetState(empty, timeout=TIMEOUT)
            except:
                return None

        return state.opened

    @classmethod
    def get_state_with_address(cls, addr):
        client = cls(addr)
        return client.get_state()
