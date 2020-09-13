import unittest

import grpc_testing
from orator import DatabaseManager

from services import room_manager_pb2
from app import RoomManagerServicer


SERVICE = room_manager_pb2.DESCRIPTOR.services_by_name['RoomManager']


# FIX 本番DBで動いてしまうのを修正する
class TestServicer(unittest.TestCase):
    def setUp(self):
        self._real_time = grpc_testing.strict_real_time()
        servicer = RoomManagerServicer()
        descriptors_to_servicers = {
            SERVICE: servicer
        }
        self._real_time_server = grpc_testing.server_from_dictionary(
            descriptors_to_servicers, self._real_time)

    def test_register(self):
        rpc = self._real_time_server.invoke_unary_unary(
            SERVICE.methods_by_name['Register'], (),
            room_manager_pb2.Room(password='test'), None)

        response, _, _, _ = rpc.termination()
        self.assertTrue(response.success)

if __name__ == '__main__':
    unittest.main()
