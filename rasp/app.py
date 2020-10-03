import json
import random
import logging
import argparse
from http import HTTPStatus
from concurrent import futures

import grpc
from flask import Flask, Response, request

from services import rasp_pb2, rasp_pb2_grpc
from raspberrypi import VirtualRasp


def get_rasp_servicer(rasp):
    class RaspServicer(rasp_pb2_grpc.RaspServicer):
        def GetState(self, request, context):
            opened = rasp.get_state()
            return rasp_pb2.State(opened=opened)
    
    return RaspServicer()


def serve_as_grpc(rasp):
    servicer = get_rasp_servicer(rasp)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rasp_pb2_grpc.add_RaspServicer_to_server(RaspServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def serve(rasp):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def get():
        opened = STATE

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
        STATE = open_

        if STATE:
            opened = True
        else:
            opened = False

        resp = {'success': True,
                'opened': opened}
        return Response(response=json.dumps(resp),
                        status=HTTPStatus.OK)

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
        serve_as_grpc(rasp)
    else:
        serve(rasp)
