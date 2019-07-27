#!env/bin/python3
import socket
import json

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


PORT = 1338


def node_request(json_obj):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", PORT))
        s.sendall(json_obj.encode())
        res = s.recv(5120)
        return res.decode()


class PendingContracts(Resource):
    def get(self, destination):
        # TODO
        return [
            {
                "Contract ID": "String",
                "Source": "String",
                "Payload": "String",
                "Amount": 56,
            }
        ]


class OutgoingContracts(Resource):
    def get(self, provider):
        # TODO
        return [
            {
                "Contract ID": "String",
                "Provider": "string",
                "Destination": "String",
                "Payload": "String",
            }
        ]


class AllContracts(Resource):
    def get(self):
        # TODO
        return [
            {
                "Contract ID": "String",
                "Source": "string",
                "Provider": "string",
                "Destination": "String",
                "Payload": "String",
            }
        ]


class VerifyContract(Resource):
    def post(self):
        # TODO
        parser = reqparse.RequestParser()
        parser.add_argument("User", type=str)
        parser.add_argument("Data", type=str)
        parser.add_argument("VerificationFailed", type=bool)
        req = json.dumps({"opcode": ""})
        args = parser.parse_args()
        return [
            {
                "User": args["User"],
                "Data": args["Data"],
                "VerificationFailed": args["VerificationFailed"],
            }
        ]


class MakeContract(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Provider", type=str)
        parser.add_argument("Source", type=str)
        parser.add_argument("Destination", type=str)
        parser.add_argument("Payload", type=str)
        parser.add_argument("Amount", type=int)
        args = parser.parse_args()
        req = json.dumps(
            {
                "opcode": "ADDCON",
                "provider": args["Provider"],
                "source": args["source"],
                "destination": args["Destination"],
                "payload": args["Payload"],
                "amount": args["Amount"]
            }
        )
        # TODO
        ret = node_request(req)
        print(ret)
        return [
            {
                "Provider": args["Provider"],
                "Source": args["Source"],
                "Destination": args["Destination"],
                "Payload": args["Payload"],
                "Amount": args["Amount"],
            }
        ]


api.add_resource(PendingContracts, "/api/pending_contracts/<string:destination>")
api.add_resource(OutgoingContracts, "/api/outgoing_contracts/<string:provider>")
api.add_resource(AllContracts, "/api/all_contracts/")
api.add_resource(VerifyContract, "/api/verify_contract/")
api.add_resource(MakeContract, "/api/make_contract/")

if __name__ == "__main__":
    app.run(port=1337, debug=True)
