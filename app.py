#!env/bin/python3
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class PendingContracts(Resource):
    def get(self, destination):
        # TODO
        return [{"Contract ID": "String", "Source": "String", "Payload": "String"}]


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
        return [
            {"User": "string",
                "Signed(Contract ID + " " + Verified Boolean)": "string"}
        ]


class MakeContract(Resource):
    def post(self):
        # TODO
        return [
            {
                "Provider": "string",
                "Source": "string",
                "Destination": "string",
                "Payload": "string",
                "Amount": 10000,
            }
        ]


api.add_resource(PendingContracts,
                 "/api/pending_contracts/<string:destination>")
api.add_resource(OutgoingContracts,
                 "/api/outgoing_contracts/<string:provider>")
api.add_resource(AllContracts, "/api/all_contracts/")
api.add_resource(VerifyContract, "/api/verify_contract/")
api.add_resource(MakeContract, "/api/make_contract/")

if __name__ == "__main__":
    app.run(debug=True)
