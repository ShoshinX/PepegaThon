import json
import hashlib
 
class Block(object):
    def __str__(self):
        return "Block " + self.index + " - " + self.data + "\n"
 
    # data passed must be a json
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = json.dumps(data)
        self.prev_hash = prev_hash
        self.curr_hash = self.get_curr_hash()

    def get_curr_hash(self):
        sha_hash = hashlib.sha256()
        # hashobject is the encoded previous hash + timestamp + the new data encoded in UTF8.
        # The internet is a nice thing
        encoded_data = self.prev_hash.encode() + self.timestamp.encode() + self.data.encode()
        sha_hash.update(encoded_data)
        # digest or hexdigest - apparently hexdigest is safer because only hex
        return sha_hash.hexdigest()
 
    def serialize(self):
        rep = {}
        rep['index'] = self.index
        rep['timestamp'] = self.index
        rep['data'] = self.data
        rep['prev_hash'] = self.prev_hash
        rep['curr_hash'] = self.curr_hash
 
        return rep