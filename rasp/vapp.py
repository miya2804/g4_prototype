import json
import logging
from http import HTTPStatus

from flask import Flask, Response, request

from raspberrypi import Rasp, VirtualRasp


class VirtualRasps():
    def __init__(self):
        self.current_id = 0
        self.vrasps_map = dict()

    def get(self):
        return self.vrasps_map

    def get_by_id(self, id_):
        return self.vrasps_map[id_]

    def register(self, vrasp):
        self.vrasps_map[str(self.current_id)] = vrasp
        id_ = self.current_id
        self.current_id += 1
        
        return id_

    def get_state_by_id(self, id_):
        return self.vrasps_map[id_].get_state()

    def set_state_by_id(self, id_, state):
        self.vrasps_map[id_].set_state(state)


def register_route(app, vrasps):
    @app.route('/api/rasp/<rasp_id>', methods=['GET'])
    def get(rasp_id):
        try:
            opened = vrasps.get_state_by_id(rasp_id)
            response = Response(response=json.dumps({'opened': opened}),
                                status=HTTPStatus.OK)

        except KeyError:
            response = Response(response='Bad Request',
                                status=HTTPStatus.BAD_REQUEST)

        return response


    @app.route('/api/rasp/<rasp_id>', methods=['POST'])
    def set(rasp_id):
        payload = request.json
        open_ = payload.get('open')
        if open_ is None:
            return Response(response='Bad Request',
                            status=HTTPStatus.BAD_REQUEST)

        try:
            vrasps.set_state_by_id(rasp_id, open_)
            response = Response(response=json.dumps({'success': True,
                                                     'opened': open_}),
                                status=HTTPStatus.OK)

        except KeyError:
            response = Response(response=json.dumps({'success': True,
                                                     'opened': None}),
                                status=HTTPStatus.BAD_REQUEST)

        except Exception:
            response = Response(response=json.dumps({'success': True,
                                                     'opened': None}),
                                status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return response


    @app.route('/api/rasp', methods=['POST'])
    def new():
        vrasp = VirtualRasp()
        id_ = vrasps.register(vrasp)
        response = Response(response=json.dumps({'success': True,
                                                 'id': id_}),
                            status=HTTPStatus.OK)
        return response


    return app


if __name__ == '__main__':
    app = Flask(__name__)
    vrasps = VirtualRasps()

    app = register_route(app, vrasps)

    app.run(host="0.0.0.0", port=8888)
