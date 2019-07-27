#!/usr/bin/python3

import asyncio
from sys import argv
import signal
import json
import base64
from node import *
from contract import Contract
from transaction import Transaction
# datetime may be obs
from datetime import datetime
from time import time
from data import generate_data
########
from verify import verify_sign

node_chain_instance = Blockchain()
# active contracts
active_contract_list = []
# get token ledger
token_ledger = (json.loads(
    node_chain_instance.block_data[-1].data)).get('ledger')
# for i in range(len(node_chain_instance.block_data)):
#    print(str(node_chain_instance.block_data[i]))


def add_contract(self, source, destination, provider, payload, amount, signedContract):
    encode_data = source.encode() + destination.encode() + provider.encode() + \
        payload.encode() + amount.encode()
######
    if not verify_sign(provider, encode_data, signedContract):
        return False
    else:
        new_contract = Contract(str(time.time()), source, destination, provider, payload, amount)
        token_ledger[source] = token_ledger[source] - new_contract.stake
        token_ledger[destination] = token_ledger[destination] - new_contract.stake
        active_contract_list.append(new_contract)

        node_chain_instance.add_block(generate_data(new_contract, None, token_ledger, active_contract_list))
        return True

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
        #res = node_chain_instance.block_data[-1].data
        self.transport.write(json.dumps(res).encode())

    def pong_handler(self, json_obj):
        # {"opcode": "PONG"}
        # handle pongs
        print(f"Ponged from {self.transport.get_extra_info('socket')}")

    def addb_handler(self, json_obj):
        # {"opcode": "ADDB", "data": <BASE64STR>}
        block = base64.decodestring(json_obj["block"])

    def addbres_handler(self, json_obj):
        # {"opcode": "ADDBRES", "bool": <Boolean>}
        pass

    def valb_handler(self, json_obj):
        # {"opcode": "VALB", "data": <BASE64STR>}
        block = base64.decodestring(json_obj["block"])

    def valbres_handler(self, json_obj):
        # {"opcode": "VALBRES", "bool": <Boolean>}
        pass

    def consensus_handler(self, json_obj):
        # {"opcode": "CONSENSUS", "data": <BASE64STR>}
        pass

    def consensusres_handler(self, json_obj):
        # {"opcode": "CONSENSUSRES", "data": <BASE64STR>}
        block = base64.decodestring(json_obj["block"])

    handler_map = {
        "PING": ping_handler,
        "PONG": pong_handler,
        "ADDB": addb_handler,
        "ADDBRES": addbres_handler,
        "VALB": valb_handler,
        "VALBRES": valbres_handler,
        "CONSENSUS": consensus_handler,
        "CONSENSUSRES": consensusres_handler,
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
