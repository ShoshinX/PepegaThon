#!/usr/bin/python3

import json
from node import *
from contract import Contract
from transaction import Transaction
import time
from data import generate_data
########
from verify import verify_sign

class Block_Interface(object):
    def __init__(self):
        self.node_chain_instance = Blockchain()
        # active contracts
        self.active_contract_list = []
        # get token ledger
        self.token_ledger = (json.loads(
            self.node_chain_instance.block_data[-1].data)).get('ledger')
        #for i in range(len(node_chain_instance.block_data)):
        #    print(str(node_chain_instance.block_data[i]))

    def get_contracts(self, public_key, search_type):
        results = {}
        if search_type == "all":
            return self.active_contract_list

        elif search_type == "outgoing":
            for i in range(len(self.active_contract_list)):
                if (self.active_contract_list[i].get('source') ==  public_key) or (self.active_contract_list[i].get('provider') == public_key):
                    results.append(self.active_contract_list[i])
            return results

        elif search_type == "incoming":
            for i in range(len(active_contract_list)):
                if self.active_contract_list[i].get('destination') ==  public_key:
                    results.append(self.active_contract_list[i])
            return results

        else:
            return None


    def add_contract(self, source, destination, provider, payload, amount, signedContract):
        encode_data = source.encode() + destination.encode() + provider.encode() + \
            payload.encode() + amount.encode()
        ######TEST
        #if not verify_sign(provider, encode_data, signedContract):
        #    return None
        #else:
        new_contract = Contract(str(time.time()), source, destination, provider, payload, amount)
        ########new_contract = Contract(str(123), source, destination, provider, payload, amount)
        self.token_ledger[source] = str(int(token_ledger[source]) - int(new_contract.stake))
        self.token_ledger[destination] = str(int(token_ledger[destination]) - int(new_contract.stake))
        self.active_contract_list.append(new_contract.serialize())

        block_data = generate_data(new_contract.serialize(), None, self.token_ledger, self.active_contract_list)
        self.node_chain_instance.add_block(block_data)

        '''
        for i in range(len(node_chain_instance.block_data)):
            print(str(node_chain_instance.block_data[i]))
        #print((json.loads(node_chain_instance.block_data[-1].data)).get('ledger'))
        print((json.loads(node_chain_instance.block_data[-1].data)))
        '''

        return block_data

    def add_transaction(self, source, destination, provider, payload, amount):

        new_trans = Transaction(str(time.time()), source, destination, provider, payload, amount)
        self.token_ledger[source] = str(int(token_ledger[source]) + int(new_trans.amount))
        self.token_ledger[destination] = str(int(token_ledger[destination]) + int(new_trans.amount))

        block_data = generate_data(None, new_trans.serialize(), self.token_ledger, self.active_contract_list)
        self.node_chain_instance.add_block(block_data)

        '''
        for i in range(len(node_chain_instance.block_data)):
            print(str(node_chain_instance.block_data[i]))
        print((json.loads(node_chain_instance.block_data[-1].data)))
        '''

        return block_data

    def settle_contract(self, contract_ID, ver_boolean, user, signature):
        encode_data = contract_ID.encode() + " ".encode() + ver_boolean.encode()
        ###
        #if not verify_sign(user, encode_data, signature):
        #    return None
        #else:
        for i in range(len(self.active_contract_list)):
            if contract_ID == self.active_contract_list[i].get('index'):
                self.active_contract_list[i]['status'] = True
                new_data = active_contract_list[i]
                self.active_contract_list.pop(i)
                return self.add_transaction(new_data.get('source'), new_data.get('destination'), new_data.get('provider'), new_data.get('payload'), new_data.get('amount'))
        return None