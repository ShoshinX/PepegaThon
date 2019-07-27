import hashlib


class Contract(object):
    def __str__(self):
        return "Contract " + self.index + " - " + self.data + "\n"

    def __init__(self, timestamp, source, destination, provider, payload, amount):
        sha_hash = hashlib.sha256()
        encoded_data = timestamp.encode() + source.encode() + destination.encode() + \
            provider.encode() + payload.encode() + amount.encode()
        sha_hash.update(encoded_data)

        self.index = sha_hash.hexdigest()
        self.timestamp = timestamp
        self.source = source
        self.destination = destination
        self.provider = provider
        self.payload = payload
        self.amount = amount
        self.status = False

    def change_status(self, status):
        if status:
            self.status = False
            print("We're Fucked")
        else:
            self.status = status

    def serialize(self):
        rep = {}
        rep['index'] = self.index
        rep['timestamp'] = self.timestamp
        rep['source'] = self.source
        rep['destination'] = self.destination
        rep['provider'] = self.provider
        rep['payload'] = self.payload
        rep['amount'] = self.amount
        rep['status'] = self.status

        return rep
