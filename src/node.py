#!/usr/bin/python3

import asyncio
from sys import argv
import signal


class SimpleBlockchainProtocol(asyncio.Protocol):

    def connection_made(self, transport: asyncio.Transport) -> None:
        loop = asyncio.get_event_loop()
        self.client_info = transport.get_extra_info("peername")
        self.transport = transport
        # Close the connection in 10 seconds if no data received.
        self.timeout_timer = loop.call_later(10, self.transport.close)

    def data_received(self, data: bytes) -> None:
        self.timeout_timer.cancel()

        self.transport.close()


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
