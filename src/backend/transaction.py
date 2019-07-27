import hashlib


class Transaction(object):
    def __str__(self):
        return "Transaction " + self.index + " - " + self.data + "\n"

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

    def serialize(self):
        rep = {}
        rep['index'] = self.index
        rep['timestamp'] = self.timestamp
        rep['source'] = self.source
        rep['destination'] = self.destination
        rep['provider'] = self.provider
        rep['payload'] = self.payload
        rep['amount'] = self.amount

        return rep
