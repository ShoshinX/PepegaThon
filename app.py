#!env/bin/python3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)


class PendingContracts(Resource):
    def get(self, destination):
        # TODO
        return [{"Contract ID": "String", "Source": "String", "Payload": "String", "Amount":56}]


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
        args = parser.parse_args()
        return [{"User": args["User"], "Data": args["Data"]}]


class MakeContract(Resource):
    def post(self):
        # TODO
        parser = reqparse.RequestParser()
        parser.add_argument("Provider", type=str)
        parser.add_argument("Source", type=str)
        parser.add_argument("Destination", type=str)
        parser.add_argument("Payload", type=str)
        parser.add_argument("Amount", type=int)
        args = parser.parse_args()
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
    app.run(port=1337,debug=True)
