import json
import random
import logging
import argparse
from http import HTTPStatus
from concurrent import futures

import grpc
from flask import Flask, Response, request

from services import rasp_pb2, rasp_pb2_grpc


class Rasp():
    def __init__(self):
        self.opened = True

    def get_state(self):
        pass

    def set_state(self, opened):
        pass


class VirtualRasp(Rasp):
    def get_state(self):
        return self.opened

    def set_state(self, opened):
        self.opened = opened


def get_rasp_servicer(rasp):
    class RaspServicer():
        def GetState(self, request, context):
            opened = rasp.get_state()
            return rasp_pb2.State(opened=opened)
    
    return RaspServicer()


def serve_as_grpc(servicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rasp_pb2_grpc.add_RaspServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def register_route(app, rasp):
    @app.route('/', methods=['GET'])
    def get():
        opened = rasp.get_state()

        resp = {'opened': opened}
        return Response(response=json.dumps(resp),
                        status=HTTPStatus.OK)

    @app.route('/', methods=['POST'])
    def set():
        payload = request.json
        open_ = payload.get('open')
        if open_ is None:
            return Response(response='Bad Request',
                            status=HTTPStatus.BAD_REQUEST)
        rasp.set_state(open_)

        resp = {'success': True,
                'opened': open_}
        return Response(response=json.dumps(resp),
                        status=HTTPStatus.OK)

    return app

def serve(rasp):
    app = Flask(__name__)

    register_route(app, rasp)

    app.run('0.0.0.0', port=3000)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grpc', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig()

    rasp = VirtualRasp()

    if args.grpc:
        servicer = get_rasp_servicer(rasp)
        serve_as_grpc(servicer)
    else:
        serve(rasp)
