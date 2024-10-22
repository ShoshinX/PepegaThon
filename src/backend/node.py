from block_struct import Block

import hashlib
import time
import json


class Blockchain(object):
    def __init__(self):
        self.block_data = []
        # find a better way to generate genesis
        self.generate_genesis()

    def validate_blockchain(self):
        for i in range(len(self.block_data)):
            sha_hash = hashlib.sha256()
            # continue if genesis block
            if i == 0:
                continue

            prev_hash = self.block_data[i - 1].curr_hash
            curr_block = self.block_data[i].data

            encoded_data = prev_hash.encode() + curr_block.encode()
            sha_hash.update(encoded_data)
            curr_hash = sha_hash.hexdigest()

            if curr_hash != self.block_data[i].curr_hash:
                return False

        return True

    def generate_genesis(self):
        with open('genesis_data.json') as json_file:
            data = json.dumps(json.load(json_file))

        genesis_block = Block(0, str(time.time(
        )), data, "Why are we still here? Just to suffer? Every night, I can feel my leg… and my arm… even my fingers. The body I’ve lost… the comrades I’ve lost… won’t stop hurting… It’s like they’re all still there. You feel it, too, don’t you?")
        
        self.block_data.append(genesis_block)

    def create_block(self, data):
        curr_block = self.block_data[-1]
        new_block = Block(curr_block.index + 1, str(time.time(
        )), data, curr_block.curr_hash)
        return new_block

    def validate_block(self, block):
        last_block = self.block_data[-1]
        veri_block = Block(last_block.index + 1, block.timestamp,
                           block.data, last_block.curr_hash)
        return veri_block.curr_hash == block.curr_hash

    def add_block(self, data):
        new_block = self.create_block(data)
        if self.validate_block(new_block):
            self.block_data.append(new_block)
            return True
        else:
            print("Add_Block Validation Failed")
            return False
