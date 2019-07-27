#!env/bin/python3
import socket
import json

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


PORT = 6969


def node_request(json_obj):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", PORT))
        s.sendall(json_obj.encode())
        res = s.recv(5120)
        return res.decode()


class PendingContracts(Resource):
    def get(self, destination):
        # TODO
        res = {"opcode": "GETINCON", "data": None}
        res['data'] = destination

        return node_request(json.dumps(res))


class OutgoingContracts(Resource):
    def get(self, provider):
        # TODO
        res = {"opcode": "GETOUTCON", "data": None}
        res['data'] = provider

        return node_request(json.dumps(res))


class AllContracts(Resource):
    def get(self):
        # TODO
        res = {"opcode": "GETALLCON", "data": None}
        
        return node_request(json.dumps(res))

class AllTransactions(Resource):
    def get(self):
        # TODO
        res = {"opcode": "GETALLTRAN", "data": None}
        
        return node_request(json.dumps(res))


class VerifyContract(Resource):
    def post(self):
        # TODO
        parser = reqparse.RequestParser()
        parser.add_argument("User", type=str)
        parser.add_argument("Data", type=str)
        parser.add_argument("ContractID", type=str)
        parser.add_argument("VerificationBoolean", type=str)
        args = parser.parse_args()

        req = {"opcode": "SETCON", "data": None}
        req['data'] = args

        return node_request(json.dumps(req))


class MakeContract(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("provider", type=str)
        parser.add_argument("source", type=str)
        parser.add_argument("destination", type=str)
        parser.add_argument("payload", type=str)
        parser.add_argument("amount", type=str)
        parser.add_argument("signedContract", type=str)
        args = parser.parse_args()
        
        req = {"opcode": "ADDCON", "data": None}
        req['data'] = args
        # TODO
        return node_request(json.dumps(req))


api.add_resource(PendingContracts, "/api/pending_contracts/<string:destination>")
api.add_resource(OutgoingContracts, "/api/outgoing_contracts/<string:provider>")
api.add_resource(AllContracts, "/api/all_contracts")
api.add_resource(AllTransactions, "/api/all_transactions")
api.add_resource(VerifyContract, "/api/verify_contract")
api.add_resource(MakeContract, "/api/make_contract")

if __name__ == "__main__":
    app.run(port=1337, debug=True)
