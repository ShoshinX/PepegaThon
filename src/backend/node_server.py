#!/usr/bin/python3

import asyncio
from sys import argv
import signal
import json
import base64
from node import *
import socket
from contract import Contract
from transaction import Transaction
import time
from data import generate_data

########
from verify import verify_sign

node_chain_instance = Blockchain()
# active contracts
active_contract_list = []
# get token ledger
token_ledger = (json.loads(node_chain_instance.block_data[-1].data)).get("ledger")

# for i in range(len(node_chain_instance.block_data)):
#    print(str(node_chain_instance.block_data[i]))


def get_contracts(public_key, search_type):
    results = {}
    if search_type == "all":
        return active_contract_list

    elif search_type == "outgoing":
        for i in range(len(active_contract_list)):
            if (active_contract_list[i].get("source") == public_key) or (
                active_contract_list[i].get("provider") == public_key
            ):
                results.append(active_contract_list[i])
        return results

    elif search_type == "incoming":
        for i in range(len(active_contract_list)):
            if active_contract_list[i].get("destination") == public_key:
                results.append(active_contract_list[i])
        return results

    else:
        return None


# Set socket timeout
socket.timeout(0.2)
# Get a list of nodes to connect to
peers = []

with open("port_list.txt", "r") as fin:
    lines = fin.readlines()
    peers = [int(x) for x in lines]


def node_request(port, json_obj):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", port))
        s.sendall(json_obj.encode())
        res = s.recv(5120)
        return res.decode()


def add_contract(source, destination, provider, payload, amount, signedContract):
    encode_data = (
        source.encode()
        + destination.encode()
        + provider.encode()
        + payload.encode()
        + amount.encode()
    )
    # TEST
    # if not verify_sign(provider, encode_data, signedContract):
    #    return None
    # else:
    ######new_contract = Contract(str(time.time()), source, destination, provider, payload, amount)
    new_contract = Contract(str(123), source, destination, provider, payload, amount)
    token_ledger[source] = str(int(token_ledger[source]) - int(new_contract.stake))
    token_ledger[destination] = str(
        int(token_ledger[destination]) - int(new_contract.stake)
    )
    active_contract_list.append(new_contract.serialize())

    block_data = generate_data(
        new_contract.serialize(), None, token_ledger, active_contract_list
    )
    node_chain_instance.add_block(block_data)

    """
    for i in range(len(node_chain_instance.block_data)):
        print(str(node_chain_instance.block_data[i]))
    #print((json.loads(node_chain_instance.block_data[-1].data)).get('ledger'))
    print((json.loads(node_chain_instance.block_data[-1].data)))
    """

    return block_data


def add_transaction(source, destination, provider, payload, amount):

    new_trans = Transaction(
        str(time.time()), source, destination, provider, payload, amount
    )
    token_ledger[source] = str(int(token_ledger[source]) + int(new_trans.amount))
    token_ledger[destination] = str(
        int(token_ledger[destination]) + int(new_trans.amount)
    )

    block_data = generate_data(
        None, new_trans.serialize(), token_ledger, active_contract_list
    )
    node_chain_instance.add_block(block_data)

    """
    for i in range(len(node_chain_instance.block_data)):
        print(str(node_chain_instance.block_data[i]))
    print((json.loads(node_chain_instance.block_data[-1].data)))
    """

    return block_data


def settle_contract(contract_ID, ver_boolean, user, signature):
    encode_data = contract_ID.encode() + " ".encode() + ver_boolean.encode()
    ###
    # if not verify_sign(user, encode_data, signature):
    #    return None
    # else:
    for i in range(len(active_contract_list)):
        if contract_ID == active_contract_list[i].get("index"):
            active_contract_list[i]["status"] = True
            new_data = active_contract_list[i]
            active_contract_list.pop(i)
            return add_transaction(
                new_data.get("source"),
                new_data.get("destination"),
                new_data.get("provider"),
                new_data.get("payload"),
                new_data.get("amount"),
            )
    return None


class SimpleBlockchainProtocol(asyncio.Protocol):
    # Kyou, why lint error? VVV
    def connection_made(self, transport: asyncio.Transport) -> None:
        loop = asyncio.get_event_loop()
        self.client_info = transport.get_extra_info("peername")
        self.transport = transport
        # Close the connection in 10 seconds if no data received.
        self.timeout_timer = loop.call_later(10, self.transport.close)

    def connection_lost(self, exc) -> None:
        pass

    def data_received(self, data: bytes) -> None:
        self.timeout_timer.cancel()
        json_obj = json.loads(data.decode())
        opcode = json_obj["opcode"]

        if opcode in self.handler_map:
            self.handler_map[opcode](self, json_obj)
            print(f"OK {opcode}")
        else:
            print(f"Invalid opcode {opcode}")

    def ping_handler(self, json_obj):
        # {"opcode": "PING"}
        print(f"Pinging {self.transport.get_extra_info('socket')}")
        # should respond with pong
        res = {"opcode": "PONG"}
        """
        print("STARTING CONTRACT\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if add_contract("E445lM216jZ4Kp1tCqWIKdeSLTA3NXwN", "UGO1pfDVmkscufjn1u4WDu5kNIBNwca0", "IFjH/fgse2+z9VDBtLDRUKUw2tfqf5b+", "water", "10000", "pog"):
            print("IT WORKED\n\n\n\n\n\n\n\n\n\n\n\n\n")

        print("settle_contract\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if settle_contract("8e651fea0b958ce0372ca8500fff99620cc76c4083ee17d834ef240fb995778e", "E445lM216jZ4Kp1tCqWIKdeSLTA3NXwN", "1", "contract_sign"):
            print("IT WORKED\n\n\n\n\n\n\n\n\n\n\n\n\n")
        else:
            print("NO SETTLE")
        quit()
        """
        res = add_contract("E445lM216jZ4Kp1tCqWIKdeSLTA3NXwN", "UGO1pfDVmkscufjn1u4WDu5kNIBNwca0", "IFjH/fgse2+z9VDBtLDRUKUw2tfqf5b+", "water", "10000", "pog")
        for peer in peers:
            if peer != int(argv[1]):
                node_request(peer, json.dumps({"opcode": "PONG"}))
                print("log_sent")

        self.transport.write(json.dumps(res).encode())

    def pong_handler(self, json_obj):
        # {"opcode": "PONG"}
        # handle pongs
        print(f"Ponged from {self.transport.get_extra_info('socket')}")

    """
    # node list
    node_list = {
        "localhost": 1337,
        "localhost": 1338
    }
    source, destination, provider, payload, amount, signedContract

    {"source":“E445lM216jZ4Kp1tCqWIKdeSLTA3NXwN", "destination":"UGO1pfDVmkscufjn1u4WDu5kNIBNwca0", "provider":"IFjH/fgse2+z9VDBtLDRUKUw2tfqf5b+", "payload":"water", "amount":"10000", "signedContract":"pog”}
    """

    def addcon_handler(self, json_obj):
        # {"opcode": "ADDCON", "data": <Dict>}
        # sample response
        res = {"opcode": "ADDCON", "data": None}

        #contract = json_obj["data"]
        '''
        res["data"] = add_contract(
            contract.get("source"),
            contract.get("destination"),
            contract.get("provider"),
            contract.get("payload"),
            contract.get("amount"),
            contract.get("signedContract"),
        )
        '''
        res["data"] = add_contract("E445lM216jZ4Kp1tCqWIKdeSLTA3NXwN", "UGO1pfDVmkscufjn1u4WDu5kNIBNwca0", "IFjH/fgse2+z9VDBtLDRUKUw2tfqf5b+", "water", "10000", "pog")

        for peer in peers:
            if peer != int(argv[1]):
                node_request(peer, json.dumps(res))
                print("log_sent")

        self.transport.write(json.dumps(res).encode())

    def setcon_handler(self, json_obj):
        # {"opcode": "ADDCON", "data": <Dict>}
        # sample response
        res = {"opcode": "SETCON", "data": None}

        contreq = json_obj["data"]
        res["data"] = settle_contract(
            contreq.get("ContractID"),
            contreq.get("VerifiedBoolean"),
            contreq.get("User"),
            contreq.get("Data")
        )

        for peer in peers:
            if peer != int(argv[1]):
                node_request(peer, json.dumps(res))

        self.transport.write(json.dumps(res).encode())

    def getallcon_handler(self, json_obj):
        # {"opcode": "GETALLCON", "data": <string>}
        # sample response
        res = {"opcode": "GETALLCON", "data": None}

        user = json_obj["data"]
        res["data"] = get_contracts(user, "all")

        self.transport.write(json.dumps(res).encode())

    def getincon_handler(self, json_obj):
        # {"opcode": "GETINCON", "data": <string>}
        # sample response
        res = {"opcode": "GETINCON", "data": None}

        user = json_obj["data"]
        res["data"] = get_contracts(user, "incoming")

        self.transport.write(json.dumps(res).encode())

    def getoutcon_handler(self, json_obj):
        # {"opcode": "GETOUTCON", "data": <string>}
        # sample response
        res = {"opcode": "GETOUTCON", "data": None}

        user = json_obj["data"]
        res["data"] = get_contracts(user, "outgoing")

        self.transport.write(json.dumps(res).encode())

    handler_map = {
        "PING": ping_handler,
        "PONG": pong_handler,
        "ADDCON": addcon_handler,
        "SETCON": setcon_handler,
        "GETALLCON": getallcon_handler,
        "GETOUTCON": getoutcon_handler,
        "GETINCON": getincon_handler
    }


async def shutdown(loop: asyncio.AbstractEventLoop):
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks)
    loop.stop()


def main(host: str, port: int) -> None:
    loop = asyncio.get_event_loop()
    coro = loop.create_server(SimpleBlockchainProtocol, host, port)

    # gracefully shutdown on ctrl+C
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, asyncio.create_task, shutdown(loop))

    loop.run_until_complete(coro)
    loop.run_forever()


if __name__ == "__main__":
    if len(argv) < 2:
        print(f"Usage: python3 {argv[0]} port")
        exit(1)

    try:
        port = int(argv[1])
    except ValueError:
        print("Please enter a valid port number.")
        exit(1)

    main("localhost", port)
